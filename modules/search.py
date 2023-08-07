import aiohttp
from brawlhalla_api import Brawlhalla
from typing import List
from colorama import Fore, Style

import disnake
from disnake import Embed, Color
from disnake.ext import commands as module
from disnake.ext.commands import Cog as Search_Module
from disnake.ui import View, Button, button
from disnake.enums import ButtonStyle
from config import BRAWLHALLA_API


class NavPlayers(View):
    def __init__(self, embeds: List[Embed]):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.index = 0

        for i, embed in enumerate(self.embeds):
            embed.set_footer(text=f"Страница {i + 1} из {len(self.embeds)}")

        self._update_state()

    def _update_state(self) -> None:
        self.prev_page.disabled = self.index == 0
        self.next_page.disabled = self.index == len(self.embeds) - 1

    @button(label="Назад", style=disnake.ButtonStyle.blurple)
    async def prev_page(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.index -= 1
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)

    @button(label="Вперед", style=disnake.ButtonStyle.blurple)
    async def next_page(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.index += 1
        self._update_state()
        await inter.response.edit_message(embed=self.embeds[self.index], view=self)


class SearchCommand(Search_Module):
    def __init__(self, bot):
        self.bot = bot

    @module.slash_command(
        name="search",
        description="Посмотреть статистику"
    )
    async def search_command(self, interaction: disnake.ApplicationCommandInteraction, 
                             name: str = module.Param(name="игрок"),
                             region: str = module.Param(name="регион", choices=["all", "eu", "us-w", "us-e", "sea", "brz", "jpn", "aus", "me", "sa"],default="all")):
        try:
            embeds = []
            index = 1

            brawl = Brawlhalla(BRAWLHALLA_API)
            players = await brawl.get_rankings(name)

            embed = Embed(
                description="Если вы обнаружили **баги**, то зайдите на **сервер** поддержки и распишите свою **ошибку**.\n" \
                            "Сервер поддержки, можно найти, написав команду: `/about`",
                color=Color.red()
            )
            embed.set_author(name="Поиск игроков", icon_url=interaction.author.display_avatar)
            embed.set_thumbnail(url=interaction.author.display_avatar)

            for player in players:
                if not region:
                    region = player.region.ALL
                elif region == "eu":
                    region = player.region.EU
                elif region == "sea":
                    region = player.region.SEA
                elif region == "brz":
                    region = player.region.BRZ
                elif region == "aus":
                    region = player.region.AUS
                elif region == "us-w":
                    region = player.region.US_W
                elif region == "us-e":
                    region = player.region.US_E
                elif region == "jpn":
                    region = player.region.JPN
                elif region == "me":
                    region = player.region.ME
                elif region == "sa":
                    region = player.region.SA

                player_field = embed.add_field(name=player.name, value=f"- Бравлхалла ID: {player.brawlhalla_id}\n- Регион: {player.region.EU}\n- Место в мировом рейтинге: {player.rank}\n- Ело: {player.rating}\n- Пик ело: {player.peak_rating}", inline=False)
                index += 1

                if index % 5 == 1:
                    embeds.append(embed)
                    embed = Embed(
                        description="Если вы обнаружили **баги**, то зайдите на **сервер** поддержки и распишите свою **ошибку**.\n" \
                                    "Сервер поддержки, можно найти, написав команду: `/about`",
                        color=Color.red()
                    )
                    embed.set_author(name="Поиск игроков", icon_url=interaction.author.display_avatar)
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                
                elif player_field == 0:
                    embeds.remove(embed)
                
            embeds.append(embed)
            await interaction.response.send_message(embed=embeds[0], view=NavPlayers(embeds))

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
    bot.add_cog(SearchCommand(bot))
