# Morpheus

I Can Only Show You The Door...

Discord bot for managing friends server.

- [discord.py](https://github.com/Rapptz/discord.py) - wrapper for Discord API
- [Docker](https://docs.docker.com) - deployment environment
- MySQL + sqlalchemy - database
- Python 3.12

## Configuration

```bash
cp config/config.template.toml config/config.toml
```

Now open the `config.toml` file in your editor. Insert the Discord API:

```toml
1 [base]
2 default_prefix = '?'
3 key = '<Your Discord API key>'
...
```

> __Be careful.__ Bad things will happen if anyone else gets a possession of this key. Do not share it with anyone, ever!

On the next two lines, insert your Discord user and server ID so you get administrator rights over the bot:

```toml
4 admin_ids = [<Your Discord user ID>]
5 guild_id = <Your Server ID here>
```

> [Where can I find my User/Server/Message ID?](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)

Then, create the following 5 channels (or use one channel for all of them) on your server and paste their IDs to the config:

```toml
11 bot_channel = <Channel ID>
12 bot_dev_channel = <Channel ID>
```

(Optional) For some features you will also need to set other config variables, usually they are divided into categories based on cogs.

### Docker setup (recommended)

Install Docker & Docker Compose V2 by going to their [official documentation](https://docs.docker.com/engine/install/). Just select your OS and follow the steps.

> You can also install Docker as a GUI App — Docker Desktop — which includes everything you need.

- If you haven't already, enable `docker` service on startup: `sudo systemctl enable --now docker.service`. Most installers should do that automatically, though.
- To use Docker without `sudo`, you also need to be in `docker` group (eg. `sudo usermod -aG docker $USER && newgrp docker`).
- It's recommended to restart your system at this point (to get all the permissions and other stuff right).

#### a. Dev containers in VS Code (one click run) — preferred option

If you are using VS Code, you can simply run Rubbergod by using the [Dev containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension.
Either by clicking on a notification or by clicking on arrows in bottom left corner (Open a Remote Window) and choosing `Reopen in container`.

#### b. Docker Compose CLI — if you don't use VS Code

This command should do the trick:

```bash
docker compose up
```

**Note:** We use the newer Compose V2 here. If the above command doesn't work, please install Compose V2: `docker-compose-plugin`. As a second option, you can install and use (now deprecated) `docker-compose` command instead.

Docker will download all the necessary stuff and run the container. If you did everything correctly, bot will connect to the DB, load all the extensions and print `Ready` at the end. It will also send `:peepowave:` emoji to the `#bot-room` if you configured one. You're now all set!

## Development

If you didn't run the container in detached mode, just press `Ctrl+C` to stop it.

Try to tweak some command a little bit and run the bot again, this time you can try to open it in detached mode so it won't block your terminal:

```bash
docker compose up --detach
```

**Note:** You can use shorter `-d` instead of `--detach`.

> If you changed some internal command logic, it should be applied instantly. If, however, your change involves Discord-side API changes — command name change, for example — it can take longer (few minutes to a few hours in extreme cases).

To stop the detached container, use this command:

```bash
docker compose down
```

### Tips (optional)

> These things are not necessary for development but can help from time to time.

#### Enable commands sync debug

To enable command synchronization debug logging, change the following setting in `morpheus.py` to `True`:

```python
command_sync_flags = commands.CommandSyncFlags()
command_sync_flags.sync_commands_debug = False
```

Database-related tips can be found in [database README](database/README.md).

List with all cogs, their commands and tasks can be found in [cog README](cogs/README.md).

## Pre-commit (useful for dev)

We have setup pre-commit in this repository. To use it use these commands:

```bash
pip install -r requirements-dev.txt
pre-commit install
```
