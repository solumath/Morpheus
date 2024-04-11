import discord

from .features import BookmarkFeatures
from .messages import BookmarkMess


class BookmarkView(discord.ui.View):
    def __init__(self, link: str = None):
        super().__init__(timeout=None)
        if link:
            self.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label="Original message", url=link))

    @discord.ui.button(emoji="🗑", style=discord.ButtonStyle.danger, custom_id="trash:delete")
    async def delete_message(self, inter: discord.Interaction, button: discord.ui.Button):
        await inter.message.delete()


class BookmarkModal(discord.ui.Modal):
    def __init__(self, message) -> None:
        super().__init__(title="Bookmark", custom_id="bookmark:tag", timeout=300)
        self.message = message

    bookmark = discord.ui.TextInput(
        label="Bookmark name",
        placeholder="Bookmark name",
        custom_id="bookmark:name",
        style=discord.TextStyle.short,
        required=False,
        max_length=200,
    )

    async def on_submit(self, inter: discord.Interaction) -> None:
        inter.message = self.message
        name = inter.data["components"][0]["components"][0].get("value", None)
        if name:
            bookmark_name = name
        else:
            bookmark_name = BookmarkMess.bookmark_created(bookmark_name=inter.guild.name)

        embed, images, files_attached = await BookmarkFeatures.create_bookmark_embed(self, inter, bookmark_name)

        try:
            if images:
                for image in images:
                    embed.append(await BookmarkFeatures.create_image_embed(self, inter, image, bookmark_name))
            await inter.user.send(
                embeds=embed,
                view=BookmarkView(inter.message.jump_url),
                files=files_attached,
            )
            await inter.response.send_message(
                BookmarkMess.bookmark_created(bookmark_name=bookmark_name),
                ephemeral=True,
            )
        except discord.HTTPException as e:
            if e.code == 50007:
                await inter.response.send_message(BookmarkMess.blocked_bot(user=inter.user.id), ephemeral=True)
            else:
                raise e
