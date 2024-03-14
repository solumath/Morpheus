import discord
from discord.ext import commands

from config.app_config import config
from custom.permission_check import is_bot_admin

from .features import get_all_cogs
from .messages import SystemMess


class SystemView(discord.ui.View):
    def __init__(self, bot: commands.Bot, count: int, cogs: list):
        super().__init__()
        self.bot = bot
        self.count = count
        self.cogs = cogs
        self.message = None
        self.selects = []

        for i in range(count):
            self.selects.append(CogSelect(bot, self, cogs[i]))
            self.add_item(self.selects[i])

    @discord.ui.button(label="Reload off", style=discord.ButtonStyle.secondary)
    async def reload_button(self, inter: discord.Interaction, button: discord.ui.Button):
        for i, _ in enumerate(self.selects):
            self.selects[i].reload = not self.selects[i].reload

        if self.selects[0].reload:
            button.style = discord.ButtonStyle.green
            button.label = "Reload on"
        else:
            button.style = discord.ButtonStyle.secondary
            button.label = "Reload off"

        await inter.response.edit_message(view=self)

    async def on_timeout(self):
        await self.message.edit(view=None)

    async def interaction_check(self, inter: discord.Interaction):
        if not is_bot_admin(False):
            await inter.response.send_message(SystemMess.not_enough_perms, ephemeral=True)
            return False
        return True


class CogSelect(discord.ui.Select):
    def __init__(self, bot: commands.Bot, view: SystemView, cogs: list):
        self.bot = bot
        self._view = view
        self.cogs = cogs
        self.reload = False
        self.message = None
        self.unloadable_cogs = ["system"]

        super().__init__(
            placeholder=self.get_initials(),
            min_values=1,
            max_values=len(self.cogs[0]),
            options=self.create_select(),
        )

    def unloaded_cogs(self) -> list[str]:
        """Return list of unloaded paths to cogs"""
        cogs = [cog for cog, _ in self.cogs]
        loaded = [cog.lower() for cog in self.bot.cogs if cog.lower() in cogs]
        return list(set(cogs) - set(loaded))

    def get_initials(self) -> str:
        """Creates placeholder for selects from names of cogs."""
        first = self.cogs[0][0]
        last = self.cogs[len(self.cogs[0]) - 1][0]
        return f"{first.title()} - {last.title()}"

    def create_select(self) -> list[discord.SelectOption]:
        """Creates one singular select from cogs"""
        options = []
        cogs = [cog for cog, _ in self.cogs]
        loaded = [cog.lower() for cog in self.bot.cogs if cog.lower() in cogs]
        loaded.sort()

        for cog, file in self.cogs:
            if cog in loaded:
                options.append(discord.SelectOption(label=cog.title(), value=cog, emoji="✅"))
            else:
                options.append(discord.SelectOption(label=cog.title(), value=cog, emoji="❌"))
        return options

    def create_embed(self, author_colour):
        def split_list(array, k):
            """Splits list into K parts of approximate equal length"""

            def index(i):
                return i * (n // k) + min(i, n % k)

            if not array:
                return []
            n = len(array)
            return [array[index(i) : index(i + 1)] for i in range(k)]

        embed = discord.Embed(title="Cogs information and loading", colour=author_colour)
        bot_cogs = [cog.lower() for cog in self.bot.cogs]
        cogs = get_all_cogs()
        cog_count = len(cogs)

        cog_loaded = []
        cog_unloaded = []
        for cog_name, _ in cogs:
            if cog_name in bot_cogs:
                if cog_name not in config.extensions:
                    cog_loaded.append(f"✅ **{cog_name.title()}**\n\n")
                else:
                    cog_loaded.append(f"✅ {cog_name.title()}\n\n")
            else:
                if cog_name in config.extensions:
                    cog_unloaded.append(f"❌ **{cog_name.title()}**\n\n")
                else:
                    cog_unloaded.append(f"❌ {cog_name.title()}\n\n")

        loaded_count = len(cog_loaded)
        unloaded_count = len(cog_unloaded)

        embed.add_field(
            name="✅ Loaded / ❌ Unloaded / 🔄 All",
            value=f"**{loaded_count} / {unloaded_count} / {cog_count}**",
            inline=False,
        )

        chunks_count = 2 if cog_count > 20 else 3

        loaded_chunks = split_list(cog_loaded, chunks_count)
        unloaded_chunks = split_list(cog_unloaded, chunks_count)

        for loaded_chunk in loaded_chunks:
            embed.add_field(name="\u200b", value="".join(loaded_chunk), inline=True)

        for unloaded_chunk in unloaded_chunks:
            embed.add_field(name="\u200b", value="".join(unloaded_chunk), inline=True)

        embed.set_footer(text="Bold items are overrides of config.extension")
        return embed

    async def callback(self, inter: discord.MessageInteraction):
        """React to user selecting cog(s)."""
        await inter.response.defer()
        if not is_bot_admin(False):
            await inter.followup.send(SystemMess.not_enough_perms, ephemeral=True)

        unloadable = [cog for cog in self.unloadable_cogs if cog in self.values]
        if unloadable:
            await inter.followup.send(SystemMess.cog_not_unloadable(cogs=", ".join(unloadable)))
            self.options = self.create_select()
            for cog in unloadable:
                self.values.remove(cog)

        if not self.reload:
            for cog in self.values:
                if cog in self.unloaded_cogs():
                    try:
                        await self.bot.load_extension(f"cogs.{cog}")
                        print(SystemMess.success_load(cogs=cog))
                    except Exception as e:
                        await inter.followup.send(f"Loading error\n`{e}`")
                else:
                    try:
                        await self.bot.unload_extension(f"cogs.{cog}")
                        print(SystemMess.success_unload(cogs=cog))
                    except Exception as e:
                        await inter.followup.send(f"Loading error\n`{e}`")
        else:
            cogs = set()
            for cog in self.values:
                try:
                    await self.bot.reload_extension(f"cogs.{cog}")
                    print(SystemMess.success_reload(cogs=cog))
                    cogs.add(cog)
                except Exception as e:
                    await inter.followup.send(f"Reloading error\n`{e}`")
            if cogs:
                await inter.followup.send(SystemMess.success_reload(cogs=", ".join(cogs)))
        self.options = self.create_select()
        await self.message.edit(embed=self.create_embed(inter.user.colour), view=self._view)
