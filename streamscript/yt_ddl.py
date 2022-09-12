from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import requests
import lxml.html
from lxml.etree import QName
from lxml import etree
from tqdm import tqdm
import av

from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
from io import BytesIO
from datetime import datetime, timedelta
import time
import re

from argparse import ArgumentParser

# init session
s = requests.Session()
retry = Retry(connect=5, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
s.mount('http://', adapter)
s.mount('https://', adapter)
get = s.get

av.logging.set_level(av.logging.PANIC)


# define exceptions
class UnparseableDatetime(BaseException):
    def __init__(self, string):
        self.string = string
        super().__init__(f"Couldn't parse datetime \"{string}\"")


class UnparseableDuration(BaseException):
    def __init__(self, string):
        self.string = string
        super().__init__(f"Couldn't parse duration \"{string}\"")


class ConsentCheckFailed(BaseException):
    def __init__(self):
        super().__init__("Didn't manage to pass consent check")


class FutureSegmentsException(BaseException):
    def __init__(self):
        super().__init__("You are requesting segments that don't exist yet!")


class Stream:
    def __init__(self, stream_type, bitrate, codec, quality, base_url):
        self.stream_type = stream_type
        self.bitrate = bitrate
        self.codec = codec
        self.quality = quality
        self.base_url = base_url

    def __str__(self):
        return f"{self.quality:{' '}{'>'}{9}} Bitrate: {self.bitrate:{' '}{'>'}{8}} Codec: {self.codec}"


class Segment:
    def __init__(self, stream, seg_num):
        self.url = stream.base_url + str(seg_num)
        self.seg_num = seg_num
        self.data = BytesIO()
        self.success = False


def local_to_utc(dt):
    if time.localtime().tm_isdst:
        return dt + timedelta(seconds=time.altzone)
    else:
        return dt + timedelta(seconds=time.timezone)


def get_mpd_data(video_url):
    req = get(video_url)
    if 'dashManifestUrl\\":\\"' in req.text:
        mpd_link = req.text.split('dashManifestUrl\\":\\"')[-1].split('\\"')[0].replace(r"\/", "/")
    elif 'dashManifestUrl":"' in req.text:
        mpd_link = req.text.split('dashManifestUrl":"')[-1].split('"')[0].replace(r"\/", "/")
    else:
        doc = lxml.html.fromstring(req.content)
        form = doc.xpath('//form[@action="https://consent.youtube.com/s"]')
        if len(form) == 0:
            raise ConsentCheckFailed()

        print("Consent check detected. Will try to pass...")
        params = form[0].xpath('.//input[@type="hidden"]')
        pars = {par.attrib['name']: par.attrib['value'] for par in params}
        s.post("https://consent.youtube.com/s", data=pars)
        return get_mpd_data(video_url)

    return get(mpd_link).text


def process_mpd(mpd_data):
    tree = etree.parse(BytesIO(mpd_data.encode()))
    root = tree.getroot()
    nsmap = {(k or "def"): v for k, v in root.nsmap.items()}
    time = root.attrib[QName(nsmap["yt"], "mpdResponseTime")]
    d_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f")
    total_seg = (
        int(root.attrib[QName(nsmap["yt"], "earliestMediaSequence")])
        + len(tree.findall(".//def:S", nsmap))
        - 1
    )
    # Float stupidity for now cause Python doesnt know how to parse this
    # TODO: Make segments actually work without these workarounds

    # sometimes, doesn't work. if not guessed correctly, will make your video longer/shorter
    # seg_len = 2
    seg_len = int(float(root.attrib["minimumUpdatePeriod"][2:-1]))
    attribute_sets = tree.findall(".//def:Period/def:AdaptationSet", nsmap)
    v_streams = []
    a_streams = []

    for a in attribute_sets:
        stream_type = a.attrib["mimeType"][0]

        for r in a.findall(".//def:Representation", nsmap):
            bitrate = int(r.attrib["bandwidth"])
            codec = r.attrib["codecs"]
            base_url = r.find(".//def:BaseURL", nsmap).text + "sq/"

            if stream_type == "a":
                quality = r.attrib["audioSamplingRate"]
                a_streams.append(Stream(stream_type, bitrate, codec, quality, base_url))
            elif stream_type == "v":
                quality = f"{r.attrib['width']}x{r.attrib['height']}"
                v_streams.append(Stream(stream_type, bitrate, codec, quality, base_url))

    a_streams.sort(key=lambda x: x.bitrate, reverse=True)
    v_streams.sort(key=lambda x: x.bitrate, reverse=True)
    return a_streams, v_streams, total_seg, d_time, seg_len


def print_info(a, v, m):
    print(f"You can go back {int(m*2/3600)} hours and {int(m*2%3600/60)} minutes...")
    print(f"Download avaliable from {datetime.today() - timedelta(seconds=m*2)}")
    print("\nAudio stream ids")
    for i in range(len(a)):
        print(f"{i}:  {str(a[i])}")

    print("\nVideo stream ids")
    for i in range(len(v)):
        print(f"{i}:  {str(v[i])}")


def download(stream, seg_range, threads=1):
    # get(seg.url).content until it's http 200
    def download_func(seg):
        while True:
            req = get(seg.url)
            if req.status_code == 200:
                break
            time.sleep(1)
        return req.content

    segments = [Segment(stream, seg) for seg in seg_range]
    results = ThreadPool(threads).imap(download_func, segments)

    combined_file = BytesIO()
    for res in tqdm(results, total=len(segments), unit="seg"):
        combined_file.write(res)

    return combined_file


def mux_to_file(output, aud, vid):
    # seek 0: https://github.com/PyAV-Org/PyAV/issues/508#issuecomment-488710828
    vid.seek(0)
    aud.seek(0)
    video = av.open(vid, "r")
    audio = av.open(aud, "r")
    output = av.open(output, "w")
    v_in = video.streams.video[0]
    a_in = audio.streams.audio[0]

    video_p = video.demux(v_in)
    audio_p = audio.demux(a_in)

    output_video = output.add_stream(template=v_in)
    output_audio = output.add_stream(template=a_in)

    last_pts = 0
    for packet in video_p:
        if packet.dts is None:
            continue

        packet.dts = last_pts
        packet.pts = last_pts
        last_pts += packet.duration

        packet.stream = output_video
        output.mux(packet)

    last_pts = 0
    for packet in audio_p:
        if packet.dts is None:
            continue

        packet.dts = last_pts
        packet.pts = last_pts
        last_pts += packet.duration

        packet.stream = output_audio
        output.mux(packet)

    output.close()
    audio.close()
    video.close()


def parse_datetime(inp, utc=True):
    formats = ["%Y-%m-%dT%H:%M", "%d.%m.%Y %H:%M", "%d.%m %H:%M", "%H:%M"]
    for fmt in formats:
        try:
            d_time = datetime.strptime(inp, fmt)
            today = datetime.today()
            if not ('d' in fmt):
                d_time = d_time.replace(year=today.year, month=today.month, day=today.day)
            if not ('Y' in fmt):
                d_time = d_time.replace(year=today.year)
            if utc:
                return d_time
            return local_to_utc(d_time)
        except ValueError:
            pass
    raise UnparseableDatetime(inp)


def parse_duration(inp):
    if (x := re.findall("([0-9]+[hmsHMS])", inp)):
        return sum(int(chunk[:-1]) * {'h': 3600, 'm': 60}.get(chunk[-1], 1) for chunk in x)
    else:
        try:
            return int(inp)
        except ValueError:
            raise UnparseableDuration(inp)


def main(parsed):

    # check -o extension
    if parsed.output and not parsed.output.endswith((".mp4", ".mkv")):
        print("Error: Unsupported output file format!")
        return 1

    start_time = None
    duration = None
    end_time = None

    # parse user-entered start, end or duration
    if parsed.start:
        start_time = parse_datetime(parsed.start, parsed.utc)
    if parsed.duration:
        duration = parse_duration(parsed.duration)
    elif parsed.end:
        end_time = parse_datetime(parsed.end, parsed.utc)

    print(start_time, duration, end_time)

    # retrieve mpd data from youtube servers
    mpd_data = get_mpd_data(parsed.url)
    a, v, m, s, ll = process_mpd(mpd_data)

    # if not -s, retrieve start time from mpd data
    if not start_time:
        start_time = s - timedelta(seconds=m * ll)
        print(start_time)
    if not duration:
        if end_time:
            duration = (end_time - (start_time or s)).total_seconds()
        else:
            duration = m * ll

    # calculate start and end segments
    start_segment = m - round((s - start_time).total_seconds() / ll)
    start_segment = max(start_segment, 0)
    end_segment = start_segment + round(duration / ll)
    if end_segment > m:
        raise FutureSegmentsException()

    print(start_time, duration, end_time)

    # just list formats if -l
    if parsed.list_formats:
        print_info(a, v, m)
        return

    # This is here until we figure out how to use youtube cookies as to not get blocked
    download_threads = min(4, parsed.download_threads or cpu_count())

    print("Downloading segments...")
    v_data = download(v[parsed.vf], range(start_segment, end_segment), download_threads)
    a_data = download(a[parsed.af], range(start_segment, end_segment), download_threads)

    print("Muxing into file...")
    mux_to_file(parsed.output, a_data, v_data)


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("-s", "--start", help="Start time of the download")
    parser.add_argument("-e", "--end", help="End time of the download")
    parser.add_argument("-d", "--duration", help="Duration of the download")
    parser.add_argument("--utc", action='store_true', help="Use UTC time instead of local")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-o", "--output", help="Output file path.")
    group.add_argument("-l", "--list-formats", action='store_true', help="List info about stream ids")
    parser.add_argument("-dt", "--download-threads", type=int, help="Set amount of download threads")
    parser.add_argument("-af", default=0, help="Select audio stream id")
    parser.add_argument("-vf", default=0, help="Select video stream id")

    parsed = parser.parse_args()

    try:
        main(parsed)
    except (UnparseableDatetime, UnparseableDuration, ConsentCheckFailed, FutureSegmentsException) as e:
        print(f'Error: {e}')
        exit(1)
