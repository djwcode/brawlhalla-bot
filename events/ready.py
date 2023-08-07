from disnake.ext import commands as event_commands
from disnake.ext.commands import Cog as Event
from database.helper import db, curs
from colorama import Style, Fore


class OnReady(Event):
    def __init__(self, bot):
        self.bot = bot

    @Event.listener("on_ready")
    async def on_ready(self):
        print(f"\n\n{Fore.RED} KABAN {Style.RESET_ALL} => Запустился!")
        curs.execute("""CREATE TABLE IF NOT EXISTS members 
            (
                id INTEGER,
                created_at INTEGER,
                kaban INTEGER,
                steam_id INTEGER,
                brawlhalla_id INTEGER
            )""")
        db.commit()


def setup(bot):
    bot.add_cog(OnReady(bot))
