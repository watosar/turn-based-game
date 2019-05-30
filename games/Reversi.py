from turn_based_game import GameManager, TurnBasedGame
from random import shuffle
from discord.ext import commands

def sum_vec2(a, b):
    return tuple(a[i]+b[i] for i in range(2))

def comvert_code_to_cood(code):
    if len(code)!=2:
        raise ValueError()
    x,y = -1,-1
    for i in code:
        if i.isdecimal():
            y = int(i)-1
        if i.isalpha():
            x = int(i, 18) - 10
    return (x, y)

class Reversi(TurnBasedGame):
    max_number_of_players = 2
    min_number_of_players = 2

    def __init__(self):
        super().__init__()
        self.board = {}
        
    def __str__(self):
        return '⏺​🇦​🇧​🇨​🇩​🇪​🇫​🇬​🇭\n'+ \
        '\n'.join(
            chr(49+y)+chr(0xfe0f)+chr(0x20e3)+''.join(
                self.players[state].disc if state!=-1 else '▪️'
                for x in range(8)
                for state in (self.board.get((x, y), -1), )
            ) for y in range(8)
        )
        
    def _dig(self, root, ang):
        print(root)
        next_coord = sum_vec2(root, ang)
        next_state = self.board.get(next_coord, -1)
        if next_state == -1:
            return False
        elif next_state is self.turn.current_turn or self._dig(next_coord, ang):
            self.board[root] = self.turn.current_turn
            return True
        return False

    def _do_reversi(self, coord):
        if self.board.get(coord, -1) != -1:
            return False
        res = 0
        for ang in ((x,y) for x in (-1,0,1) for y in (-1,0,1) if x|y):
            next_coord = sum_vec2(coord,ang)
            if self.board.get(next_coord) == self.turn.current_turn^1:
                res += self._dig(next_coord, ang)
        if res:
            self.board[coord] = self.turn.current_turn
        return res

    def init_game(self):
        super().init_game()
        self.board = (
            {
                (3, 3): 1, (4, 3): 0,
                (3, 4): 0, (4, 4): 1,
            }
        )
        shuffle(self.players)
        for i, pl in enumerate(self.players):
            if getattr(pl, 'disc', None):
                continue
            pl.disc = ('🔴', '⚪️')[i]
    def _close(self):
        self.is_end = True
        
    def play(self, action):
        super().play()
        coord = comvert_code_to_cood(action)
        res = self._do_reversi(coord)
        if not res:
            raise ValueError('uncorrect coord')
        if len(self.board) == 64:
            self._close()
        next(self.turn)


class ReversiGameManager(GameManager):
    def __init__(self):
        super().__init__(Reversi())

    def init_game(self):
        self.game.init_game()
    
    def get_result(self):
        if not self.game.is_end:
            return 
        check = tuple(self.game.board.values()).count(0)
        winner = None
        if check > 32:
            winner = self.game.players[0]
        elif check < 33:
            winner = self.game.players[1]
            
        if winner:
            return 'winner is {winner}; {check} : {64-check}'
        else:
            return 'draw'

    def format_game_board(self):
        board = str(self.game)
        disc = self.game.current_player.disc
        suggest = f'--next turn info--\nmember: {self.get_current_turn_member()}, disc: {disc}\n------------------'
        return f'{board}\n{suggest}'

    def play(self, member, action):
        self.member_turn_manager.play(member, action)
        return self.format_game_board()


class ReversiCog(commands.Cog):
    @commands.command()
    async def reversi(self, ctx):
        ...

