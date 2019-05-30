from turn_based_game import GameManager, TurnBasedGame
from random import shuffle


class Reversi(TurnBasedGame):
    max_number_of_players = 2
    min_number_of_players = 2

    def __init__(self):
        super().__init__()
        self.board = {}

    def __str__(self):
        return ''

    def init_game(self):
        super().init_game()
        self.board = (
            {
                (3, 3): 1, (4, 3): -1,
                (3, 4): -1, (4, 4): 1,
            }
        )
        shuffle(self.players)

    def play(self, action):
        super().play(action)
        ...
        next(self.turn)

    def _dig(self, coord):
        ...

    def _do_reversi(self, coord):
        ...


class ReversiGameManager(GameManager):
    def __init__(self):
        super().__init__(Reversi())

    def init_game(self):
        self.game.init_game()

    def format_game_board(self):
        return '@ABCDEFGH\n'+'\n'.join(chr(49)+i+column for i, column in zip(range(8), str(self.game)))

    def play(self, member, action):
        self.member_turn_manager.play(member, action)
        return self.format_game_board()
