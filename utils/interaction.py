import discord


async def custom_send(
    inter: discord.Interaction,
    content: str = None,
    ephemeral: bool = False,
    embed: discord.Embed = None,
    edit: bool = True,
    **kwargs,
) -> None:
    """Send a message for the interaction or edit the original response if it's already done."""
    if inter.response.is_done() and edit:
        await inter.edit_original_response(content=content, embed=embed, **kwargs)
    elif inter.response.is_done():
        await inter.followup.send(content=content, embed=embed, ephemeral=ephemeral, **kwargs)
    else:
        await inter.response.send_message(content=content, embed=embed, ephemeral=ephemeral, **kwargs)
