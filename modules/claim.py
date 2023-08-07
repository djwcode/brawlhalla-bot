import aiohttp

import disnake
from disnake import Embed, Color
from disnake import ButtonStyle
from disnake.ui import Button
from disnake.ext import commands as module
from disnake.ext.commands import Cog as Claim_Module
from disnake.ext.commands import Param
from database.helper import add_steam, curs
from config import STEAM_API


class ClaimCommand(Claim_Module):
    def __init__(self, bot):
        self.bot = bot

    @module.slash_command(
        name="claim",
        description="Подключить свой аккаунт"
    )
    async def claim_command(self,
                            interaction,
                            steam_id: str = Param(name="id",
                                                  description="Укажите индификатор аккаунта стима"
                                                  )
                            ):
        user = interaction.author
        steam_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API}&steamids={steam_id}"

        async with aiohttp.ClientSession() as session:
            response = await session.get(steam_url)
            data = await response.json()
            user_info = data["response"]["players"][0]

        emb = Embed(
            description=f"Я нашел акккаунт: `{user_info['personaname']}`\n"
                        f"Стим индификатор: `{user_info['steamid']}`\n"
                        f"Аккаунт создан: <t:{user_info['timecreated']}:d>\n\n"
                        f"Это ваш аккаунт, если да, то нажмите на кнопку `Подключить`",
            color=Color.red()
        )
        emb.set_author(name="Кабанчик » Подключение аккаунта", icon_url=self.bot.user.display_avatar.url)
        emb.set_thumbnail(url=user_info['avatarfull'])
        emb.set_footer(text="Кабанчик - Хрю...")
        await interaction.response.send_message(embed=emb, components=[
            Button(label="Подключить", style=ButtonStyle.green, custom_id="claim_button"),
            Button(label="Посмотреть профиль", style=ButtonStyle.link, url=user_info['profileurl']),
            Button(label="Отмена", style=ButtonStyle.red, custom_id="cancel_button")
        ])

    @Claim_Module.listener("on_button_click")
    async def on_button_click(self, interaction: disnake.MessageInteraction):
        if interaction.component.custom_id == "claim_button":
            if curs.execute("SELECT steam_id FROM users WHERE id = ?", (interaction.author.id,)).fetchone() is None:
                add_steam(interaction.author.id, interaction.user.id)
                emb = Embed(
                    description=f"Вы подключили свой аккаунт стим!",
                    color=Color.red()
                )
                emb.set_author(name="Кабанчик » Подключение аккаунта", icon_url=self.bot.user.display_avatar.url)
                emb.set_thumbnail(url=interaction.author.display_avatar.url)
                emb.set_footer(text="Кабанчик - Хрю...")
                await interaction.response.send_message(embed=emb)
            else:
                emb = Embed(
                    description=f"Кабанья пропасть! Не удалось подключить аккаунт к стиму. Какой-то кабан занял твой "
                                f"стим аккаунт.",
                    color=Color.red()
                )
                emb.set_author(name="Кабанчик » Подключение аккаунта", icon_url=self.bot.user.display_avatar.url)
                emb.set_thumbnail(url=interaction.author.display_avatar.url)
                emb.set_footer(text="Кабанчик - Хрю...")
                await interaction.response.send_message(embed=emb)

        elif interaction.component.custom_id == "cancel_button":
            await interaction.response.delete()


def setup(bot):
    bot.add_cog(ClaimCommand(bot))
