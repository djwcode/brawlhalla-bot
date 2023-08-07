from disnake import Embed, Color
from disnake.ext import commands as module
from disnake.ext.commands import Cog as Help_Module


class HelpCommand(Help_Module):
    def __init__(self, bot):
        self.bot = bot

    @module.slash_command(
        name="help",
        description="Посмотреть список команд"
    )
    async def help_command(self, interaction):
        emb = Embed(
            description="Чтобы использовать команды, вам нужно поставить `/` и выбрать в списке необходимую команду. "
                        "Также если вы обнаружили баги, то зайдите на сервер поддержки и распишите свою ошибку."
                        "\n\n"
                        "**Команды бота**\n"
                        "`/help`, `/about`, `/ping`, `/invite`, `/invite_link`, `/support`\n\n"
                        "**Информационные команды**\n"
                        "`/userinfo`, `/serverinfo`, `/bhnews`, `/kaban_link`\n\n"
                        "**Бравлхалла**\n"
                        "`/claim`, `/stats`, `/rank`\n",
            color=Color.red()
        )
        emb.set_author(name="Кабанчик » Команды", icon_url=self.bot.user.display_avatar.url)
        emb.set_footer(text="Кабанчик - Хрю...")
        await interaction.response.send_message(embed=emb)


def setup(bot):
    bot.add_cog(HelpCommand(bot))
