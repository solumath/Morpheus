FROM python:3.9-alpine3.13

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add gcc g++ musl-dev ffmpeg-dev git

WORKDIR /morpheus
RUN mkdir -p /morpheus/servers/logs

RUN /usr/local/bin/python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN git config --global --add safe.directory /morpheus

ENTRYPOINT [ "python3", "bot.py" ]
