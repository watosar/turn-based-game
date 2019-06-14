import asyncio
import logging
import os
import discord
from discord.ext import commands
from games import GameManager, Reversi, Quarto

logging.basicConfig(level=logging.INFO)
asyncio.set_event_loop(asyncio.new_event_loop())


bot = commands.Bot(command_prefix='!bg')
bot.games = dict()


@bot.event
async def on_ready():
    print('logged on as', bot.user)
    print(bot.guilds)
    

@bot.event
async def _init_game(ctx, game, members):
    if ctx.channel.id in bot.games:
        await ctx.channel.send('already a game exists in this channel')
        return
    
    game_manager = GameManager(gamr)
    self.bot.games[ctx.channel.id] = game_manager
    
    for m in members:
        try:
            game_manager.register_player(m.id)
        except ValueError as e:
            await ctx.channel.send(e)
            break
        
    if len(game_manager.players) == game_manager.game.max_number_of_players:
        game.init_game()
        await ctx.channel.send(f'game started\nplayers: {", ".join(f"<@{i}>" for i in game.members.values())}')
    else:
        await ctx.channel.send('waiting for more player registered')
    
    
@bot.command()
async def start(ctx):
    game = bot.games.get(ctx.channel.id, None)
    if not game:
        await ctx.channel.send('no game is here') 
    elif game.is_open:
        await ctx.channel.send('game already started')
    else:
        try:
            game.init_game()
            await ctx.channel.send(f'game started\nplayers: {", ".join(f"<@{i}>" for i in game.members.values())}')
        except ValueError as e:
            await ctx.channel.send(e)
        
    
@bot.command()
async def end(ctx):
    game = bot.games.pop(ctx.channel.id, None)
    if not game:
        await ctx.channel.send('no game is here')
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
        
@commands.Cog.listener()
async def on_message(self, message):
    game = self.bot.games.get(message.channel.id)
    if not game or not game.is_open or message.author.id not in game.members.values():
        return 
    result = game.play(message.author.id, message.content)
    await message.channel.send(result)
        
        
        
bot.add_cog(Reversi.Cog(bot))
bot.add_cog(Quarto.Cog(bot))

bot.run(os.environ['token'])

