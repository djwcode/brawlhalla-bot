import aiohttp
from brawlhalla_api import Brawlhalla
from colorama import Fore, Style

import disnake
from disnake import Embed, Color
from disnake.ext import commands as module
from disnake.ext.commands import Cog as Rank_Module
from disnake.ui import Button
from disnake.enums import ButtonStyle
from config import BRAWLHALLA_API


class RankCommand(Rank_Module):
    def __init__(self, bot):
        self.bot = bot

    @module.slash_command(
        name="rank",
        description="Посмотреть статистику"
    )
    async def rank_command(self, interaction: disnake.ApplicationCommandInteraction, name):
        try:
            brawl = Brawlhalla(BRAWLHALLA_API)
            players = await brawl.get_rankings(name)
            brawluser_id = players[0].brawlhalla_id
            stats = await brawl.get_stats(int(brawluser_id))

            image = "https://i.imgur.com/Xa3fJ9K.jpg"

            if not players[0].tier:
                image = "https://i.imgur.com/Xa3fJ9K.jpg"
            

            embed = Embed(
                title=f"**Рейтинг игрока — {players[0].name}**",
                color=Color.red()
            )
            embed.set_author(name="Ранкед, хрю...", icon_url=interaction.author.display_avatar)
            embed.add_field(name="Информация об игроке", value=f"- **Индификатор:** {int(brawluser_id)}\n- **Никнейм**: {players[0].name}\n- **Регион**: {players[0].region}\n- **Звание**: {players[0].tier}\n", inline=True)
            embed.add_field(name="Рейтинг игрока", value=f"- **Ело:** {players[0].rating}\n- **Пик Ело**: {players[0].peak_rating}\n- **Статистика**:\n - Побед: {players[0].wins}\n - Поражений: {players[0].games - players[0].wins}\n - Игр: {players[0].games}\n - Винрейт: {round(players[0].wins / players[0].games * 100, 1)} %", inline=True)
            embed.add_field(name="Дополнительная информация", value=f"- **Клан:** {stats.clan.clan_name}\n- **Опыт клана:** {stats.clan.clan_xp}", inline=False)
            embed.set_thumbnail(url=interaction.author.display_avatar)
            embed.set_footer(text="Кабанчик - Хрю...")
            await interaction.response.send_message(embed=embed, components=[
                Button(label="Посмотреть", style=ButtonStyle.link, url=f"https://corehalla.com/stats/player/{brawluser_id}")
            ])

        except Exception as e:
            print(f"{Fore.BLACK} KABAN {Style.RESET_ALL} => {e}!")
            embed = Embed(
                description="Хрю... Не нашел такого человека! Возможно вы ошиблись или произошла ошибка!\n",
                color=Color.red()
            )
            embed.set_author(name="Поиск игроков", icon_url=interaction.author.display_avatar)
            embed.set_thumbnail(url=interaction.author.display_avatar)
            await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(RankCommand(bot))
