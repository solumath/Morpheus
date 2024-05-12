from __future__ import annotations

from typing import TYPE_CHECKING

from .cog import Weather

if TYPE_CHECKING:
    from morpheus import Morpheus


async def setup(bot: Morpheus):
    await bot.add_cog(Weather(bot))
