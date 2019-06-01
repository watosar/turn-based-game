import asyncio
import logging
import os
import discord
from discord.ext import commands
from games import Reversi, Quarto

logging.basicConfig(level=logging.INFO)
asyncio.set_event_loop(asyncio.new_event_loop())


bot = commands.Bot(command_prefix='!bg')
bot.games = dict()


@bot.event
async def on_ready():
    print('logged on as', bot.user)
    

@bot.event
async def _init_game(ctx, game_class, members):
    if ctx.channel.id in bot.games:
        await ctx.channel.send('already a game exists in this channel')
        return
        
    game = game_class()
    self.bot.games[ctx.channel.id] = game_class()
    
    for m in members:
        try:
            game.register_member(m.id)
        except ValueError as e:
            await ctx.channel.send(e)
            break
        
    if len(game.members) == game.max_number_of_players:
        game.init_game()
    else:
        await ctx.channel.send('waiting for more player registered')
    
    
@bot.command()
async def start(ctx):
    game = bot.games.get(ctx.channel.id, None)
    if not game:
        ...
        return 
    
    game.init_game()
    
    
@bot.command()
async def end(ctx):
    game = bot.games.pop(ctx.channel.id, None)
    if not game:
        ...
        return 
    await ctx.channel.send('ended game')
    
    
@bot.command()
async def register(ctx, members: commands.Greedy[discord.Member]):
    game = self.bot.games.get(message.channel.id)
    if not game or game.is_open:
        return 
    for m in members:
        try:
            game.register_member(m.id)
        except ValueError as e:
            await ctx.channel.send(e)
            break
    # if players is max → game start
    # else wait
        
        
bot.add_cog(Reversi.Cog(bot))
bot.add_cog(Quarto.Cog(bot))

#bot.run(os.environ['token'])

