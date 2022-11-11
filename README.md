# Morpheus

I Can Only Show You The Door...

Discord bot for managing school server.

## Pre-commit (useful for dev)

We have setup pre-commit in this repository. To use it use these commands:

```bash
pip install -r requirements-dev.txt
pre-commit install
```

## Docker compose setup (recomended)

Install `docker` and `docker-compose` for your system (will vary from system to system)
and run `docker` (`systemctl start docker.service`)

To run docker user needs to be in `docker` group. (eg. `sudo usermod -aG docker $USER`).

```bash
docker build .
```

and then everytime you want to run the app

```bash
docker-compose down && docker-compose up --build
```

## Local setup

Needed Python 3.8+

1. install requirements

    ```bash
    pip3 install -r requirements.txt
    ```

2. create folders servers/logs/
3. run

    ```bash
    python3 bot.py
    ```
