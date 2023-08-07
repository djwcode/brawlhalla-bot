import disnake
from os import listdir
from disnake.ext import commands
from disnake.ext.commands import Bot as Client
from config import TOKEN


bot = Client(command_prefix=commands.when_mentioned, intents=disnake.Intents.all(), help_command=None)


for module in listdir("./modules"):
    if module.endswith(".py"):
        bot.load_extension(f"modules.{module[:-3]}")

for event in listdir("./events"):
    if event.endswith(".py"):
        bot.load_extension(f"events.{event[:-3]}")


bot.run(TOKEN)
