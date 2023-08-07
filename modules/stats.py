import aiohttp
from brawlhalla_api import Brawlhalla

import disnake
from disnake import Embed
from disnake.ext import commands as module
from disnake.ext.commands import Cog as Stats_Module
from config import BRAWLHALLA_API


class StatsCommand(Stats_Module):
    def __init__(self, bot):
        self.bot = bot

    @module.slash_command(
        name="stats",
        description="Посмотреть статистику"
    )
    async def stats_command(self, interaction: disnake.ApplicationCommandInteraction, name):
        brawl = Brawlhalla(BRAWLHALLA_API)
        players = await brawl.get_rankings(name)

        embed = Embed(
            description=f"Вы просматриваете профиль игрока: {players[0].name}"
        )
        embed.set_author("Статистика", icon_url=interaction.author.display_avatar)


def setup(bot):
    bot.add_cog(StatsCommand(bot))
