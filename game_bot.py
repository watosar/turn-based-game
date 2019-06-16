import asyncio
import logging
import os
import discord
from discord.ext import commands
from games import GameManager, Reversi#, Quarto
logging.basicConfig(level=logging.INFO)
asyncio.set_event_loop(asyncio.new_event_loop())


bot = commands.Bot(command_prefix='!bg ')
bot.game_managers = dict()


@bot.event
async def on_ready():
    print('logged on as', bot.user)
    print(bot.guilds)


@bot.event
async def on_message(message):
    if message.content.startswith(bot.command_prefix):
        print('process commands')
        await bot.process_commands(message)
        return
    
    game = bot.game_managers.get(message.channel.id)
    if not game or not game.is_open or message.author.id not in game.members.values():
        return 
    result = game.play(message.author.id, message.content)
    await message.channel.send(result)
    

@bot.listen()
async def on_command_error(ctx, error):
    await ctx.channel.send(str(error))
    print(error)
    

@bot.event
async def _init_game(ctx, game, members):
    if ctx.channel.id in bot.game_managers:
        await ctx.channel.send('already a game exists in this channel')
        return
    
    game_manager = GameManager(game)
    self.bot.game_managers[ctx.channel.id] = game_manager
    
    for m in members:
        try:
            game_manager.register_player(m.id)
        except ValueError as e:
            await ctx.channel.send(e)
            break
        
    if len(game_manager.players) == game_manager.game.max_number_of_players:
        await ctx.channel.send(f'starting game\nfor players: {", ".join(f"<@{i}>" for i in game.members.values())}')
        await bot.start(ctx)
    else:
        await ctx.channel.send('waiting for more player registered')
    
    
@bot.command()
async def start(ctx):
    print('command: start')
    game_manager = bot.game_managers.get(ctx.channel.id, None)
    if not game_manager:
        raise ValueError('no game is here') 
    
    game_manager.start()
    await ctx.channel.send(f'game started\nplayers: {", ".join(f"<@{i}>" for i in game.members.values())}')

        
@bot.command()
async def stop(ctx):
    game_manager = bot.game_managers.pop(ctx.channel.id, None)
    if not game_manager:
        await ctx.channel.send('no game is here')
        return 
    del game_manager
    await ctx.channel.send('ended game')
    
    
@bot.command()
async def register(ctx, members: commands.Greedy[discord.Member]):
    game_manager = self.bot.game_managers.get(message.channel.id)
    if not game_manager or game_manager.is_started:
        raise ValueError('game is already started')
    for m in members:
        try:
            game.register_member(m.id)
        except ValueError as e:
            await ctx.channel.send(e)
            break
    # if players is max → game start
    # else wait
    
        
bot.add_cog(Reversi.Cog(bot))
#bot.add_cog(Quarto.Cog(bot))

bot.run(os.environ['token'])

