import discord
from discord.ext import commands

from custom.permission_check import is_bot_admin

from . import features
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
    async def reload_button(self, inter: discord.Interaction, button: discord.ui.Button) -> None:
        for i, _ in enumerate(self.selects):
            self.selects[i].reload = not self.selects[i].reload

        if self.selects[0].reload:
            button.style = discord.ButtonStyle.green
            button.label = "Reload on"
        else:
            button.style = discord.ButtonStyle.secondary
            button.label = "Reload off"

        await inter.response.edit_message(view=self)

    async def on_timeout(self) -> None:
        await self.message.edit(view=None)

    async def interaction_check(self, inter: discord.Interaction) -> bool:
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
            max_values=len(self.cogs),
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
        last = self.cogs[len(self.cogs) - 1][0]
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

    async def callback(self, inter: discord.MessageInteraction) -> None:
        """React to user selecting cog(s)."""
        await inter.response.defer()
        if not is_bot_admin(False):
            await inter.followup.send(SystemMess.not_enough_perms, ephemeral=True)
            return

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
                        await inter.followup.send(f"Unloading error\n`{e}`")
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
        await self.message.edit(embed=features.create_embed(self.bot), view=self._view)
