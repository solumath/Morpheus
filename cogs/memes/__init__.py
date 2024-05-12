from __future__ import annotations

from typing import TYPE_CHECKING

from .cog import Memes

if TYPE_CHECKING:
    from morpheus import Morpheus


async def setup(bot: Morpheus):
    await bot.add_cog(Memes(bot))
