# Morpheus
I Can Only Show You The Door...

Discord bot for managing school server.

## Docker compose setup (recomended)

Install `docker` and `docker-compose` for your system (will vary from system to system)
and run `docker` (`systemctl start docker.service`)

To run docker user needs to be in `docker` group. (eg. `sudo usermod -aG docker $USER`).

```
docker build .
```

and then everytime you want to run the app

```
docker-compose down && docker-compose up --build
```

## Local setup 
Needed Python 3.8+

1. install requirements
```
pip3 install -r requirements.txt
```

2. create folders servers/logs/
3. run

```
python3 bot.py
```
