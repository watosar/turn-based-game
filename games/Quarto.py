from turn_based_game import GameManager, TurnBasedGame
from random import shuffle
import discord
from discord.ext import commands

str_board_base = '''\
▪️▪️▪️🇦▪️▪️▪️
▪️▪️🇧▪️🇨▪️▪️
▪️🇩▪️🇪▪️🇫▪️
🇬▪️🇭▪️🇮▪️🇯
▪️🇰▪️🇱▪️🇲▪️
▪️▪️🇳▪️🇴▪️▪️
▪️▪️▪️🇵▪️▪️▪️
'''

_internal_str_board = '''\
▪️▪️▪️00▪️▪️▪️
▪️▪️01▪️04▪️▪️
▪️02▪️05▪️08▪️
03▪️06▪️09▪️12
▪️07▪️10▪️13▪️
▪️▪️11▪️14▪️▪️
▪️▪️▪️15▪️▪️▪️
'''

translate_table = {0: 0, 1: 1, 2: 4, 3: 2, 4: 5, 5: 8, 6: 3, 7: 6, 8: 9, 9: 12, 10: 7, 11: 10, 12: 13, 13: 11, 14: 14, 15: 15}
piece_table = ('<:00:583671042111963139>', '<:01:583671101771481098>', '<:02:583671169744502784>', '<:03:583671241026830354>', '<:04:583671308223774730>', '<:05:583671353505480714>', '<:06:583671439589244952>', '<:07:583671483965112338>', '<:08:583671600495198215>', '<:09:583671648733888556>', '<:10:583671760201842708>', '<:11:583671797111717888>', '<:12:583671855815196704>', '<:13:583672315410382860>', '<:14:583672360905867265>', '<:15:583672398092697621>')

class Quarto(TurnBasedGame):
    '''
    0b0000, 0b0001, 0b0010, 0b0011, 0b0100, 0b0101, 0b0110, 0b0111, 
    0b1000, 0b1001, 0b1010, 0b1011, 0b1100, 0b1101, 0b1110, 0b1111
    '''
    max_number_of_players = 2
    min_number_of_players = 2
    
    def __init__(self):
        super().__init__()
        self.board = [None]*16
        self.rest_pieces = [i for i in range(16)]
        self.selected = None
        
    def __str__(self):
        str_board = str_board_base
        for i in range(16):
            value = self.board[translate_table[i]]
            if value is None:
                value = format(i, '02')
            else:
                value = piece_table[value]
            str_board = str_board.replace(format(i,'02'), value)
        return str_board
        
    def _close(self):
        self.is_end = True
    
    def init_game(self):
        super().init_game()
        shuffle(self.players)
        
    def _check_quarto(self):
        for r, c in ((1,4),(4,1)):
            for i in range(4):
                piece = self.board[i]
                if piece is None:
                    continue
                f_check = t_check = piece
                for a in range(4):
                    piece = self.board[i*r+a*c]
                    if piece is None:
                        break
                    t_check &= piece
                    f_check |= piece
                else:
                    if t_check or not f_check:
                        self._close()
                        return True
        return False
        
    def play(self, action):
        super().play()
        if not isinstance(action, str):
            raise TypeError()
            
        if self.selected is None and (action.startswith('クアルト') or action.lower().startswith('quarto')):
            result = self._check_quarto()
            return ('Not Quarto...','Quarto!!')[result]
        
        if self.selected is None:
            if not action.isdecimal():
                raise ValueError('invaild command')
            
            num = int(action)
            self.rest_pieces.remove(num)
            self.selected = num
            next(self.turn)
        else:
            if not action.isalpha():
                raise ValueError('invaild command')
            num = int(action, 26)-10
            num = translate_table[num]
            self.board[num], self.selected = self.selected, None
        
    
class QuartoGameManager(GameManager):
    def __init__(self):
        super().__init__(Quarto())
        
    def init_game(self):
        self.game.init_game()
        
    def get_result(self):
        if not self.game.is_end:
            return 
        winner = self.get_current_turn_member()
        return f'winner is: {winner}'
    
    def format_game_board(self, addition = ''):
        if not self.game.is_end:
            if self.game.selected is not None:
                info = f'selected piece: {self.game.selected}\nselect position to put'
            else:
                info = f'select in: {[piece_table[i].replace(":",":_",1) for i in  self.game.rest_pieces]}\nor say Quarto!'
            info = f'--next turn info--\nmember: {self.member_turn_manager.current_turn_member}\n{info}'
        else:
            info = f'--this game is end--\n{self.get_result()}\n--------------------'
        return f'{addition+chr(10)*2}{str(self.game)}\n{info}'
        
    def play(self, member, action):
        result = self.member_turn_manager.play(member, action)
        return self.format_game_board(result or '')
        
        
class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def quarto(self, ctx, member1:discord.Member =None, member2:discord.Member =None):
        if ctx.channel.id in self.bot.games:
            await ctx.channel.send('already a game exists in this channel')
            return
        game = QuartoGameManager()
        self.bot.games[ctx.channel.id] = game
        
        if member1:
            game.register_member(member1.id)
        if member2:
            game.register_member(member2.id)
            game.init_game()
        
    @commands.command()
    async def register(self, ctx, member1:discord.Member, member2:discord.Member =None):
        game = self.bot.games.get(message.channel.id)
        if not game or game.is_open:
            return 
        game.register_member(member1)
        if member2:
            game.register_member(member2)
        
        if len(game.members)==2:
            game.init_game()
        
    @commands.Cog.add_listener()
    async def on_message(self, message):
        game = self.bot.games.get(message.channel.id)
        if not game or not game.is_open:
            return 
        result = game.play(message.author.id, message.content)
        await message.channel.send(result)

