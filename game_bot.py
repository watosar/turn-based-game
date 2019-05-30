import asyncio
import logging
import os
from discord.ext import commands

logging.basicConfig(level=logging.INFO)
asyncio.set_event_loop(asyncio.new_event_loop())


bot = commands.Bot(command_prefix='bg')
@bot.event
async def on_ready():
    print('logged on as', bot.user)

bot.add_cog()
bot.run(os.environ['token'])
