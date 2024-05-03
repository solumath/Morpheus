import discord


async def custom_send(
    inter: discord.Interaction, content: str, ephemeral: bool = False, edit: bool = True, **kwargs
) -> None:
    """Send a message for the interaction or edit the original response if it's already done."""
    if inter.response.is_done() and edit:
        await inter.edit_original_response(content=content, **kwargs)
    elif inter.response.is_done():
        await inter.followup.send(content=content, ephemeral=ephemeral, **kwargs)
    else:
        await inter.response.send_message(content=content, ephemeral=ephemeral, **kwargs)
