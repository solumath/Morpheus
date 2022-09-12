from disnake.ext import commands
from features.reaction_context import ReactionContext
from cogs.bookmark import Bookmark


class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_raw_reaction_add")
    async def bookmark(self, payload):
        ctx: ReactionContext = await ReactionContext.from_payload(self.bot, payload)
        if ctx is None:
            return

        if ctx.emoji == "🔖":
            await Bookmark.bookmark_reaction(self.bot, ctx)


def setup(bot):
    bot.add_cog(Reactions(bot))
