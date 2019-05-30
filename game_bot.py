import asyncio
import logging
import os
from discord.ext import commands
from games import Reversi
logging.basicConfig(level=logging.INFO)
asyncio.set_event_loop(asyncio.new_event_loop())


bot = commands.Bot(command_prefix='!bg')

bot.games = dict()

@bot.event
async def on_ready():
    print('logged on as', bot.user)

bot.add_cog(Reversi.Cog(bot))

bot.run(os.environ['token'])

