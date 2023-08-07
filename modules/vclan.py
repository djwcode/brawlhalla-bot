import aiohttp
from brawlhalla_api import Brawlhalla

import disnake
from disnake import Embed
from disnake.ext import commands as module
from disnake.ext.commands import Cog as Clan_Module
from config import BRAWLHALLA_API


class VClanCommand(Clan_Module):
    def __init__(self, bot):
        self.bot = bot

    @module.slash_command(
        name="vclan",
        description="Посмотреть наш клан"
    )
    async def vclan_command(self, interaction: disnake.ApplicationCommandInteraction):

        embed = Embed(
            color=disnake.Color.red(),
            description=f"Искали один из хороших кланов?\nПерспективный и новый клан, где постоянно сидят активные, сильные и просто веселые пареньки, тогда тебе к нам!"
        )
        embed.set_author(name="Хрю..Кланчик", icon_url=interaction.author.display_avatar)
        embed.set_footer(text="Кабанчик - Хрю...")
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(VClanCommand(bot))
