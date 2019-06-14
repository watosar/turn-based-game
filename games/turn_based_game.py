import random


class Turn:
    def __init__(self, size=1):
        if size < 1:
            raise ValueError(f'size must be positive integer, not {size}')
        self._turn_count = 0
        self.loop_size = size
    
    def update_loop_size(self, size: int):
        if not isinstance(size, int):
            raise TypeError(f'size must be int not {type(size)}')
        self.loop_size = size

    def current(self):
        return self._turn_count % self.loop_size

    def __next__(self):
        self._turn_count += 1


class Player:
    def __init__(self, member):
        self.member = member

    def __setattr__(self, key, value):
        if key == 'member':
            raise TypeError()

    def __eq__(self, other):
        return other == self.member


class TurnManager:
    def __init__(self):
        self.turn = Turn()
        self.players = []
        self.is_started = False

    def start(self):
        self.turn.update_loop_size(len(self.players))
        self.is_started = True
    
    def register_player(self, member):
        player = Player(member)
        self.players.append(player)

    def shuffle(self):
        random.shuffle(self.players)

    def get_current_turn_player(self):
        return self.players[self.turn.current()]


class GameManager:
    def __init__(self, game, *, turn_manager=None):
        self._turn_manager = turn_manager or TurnManager()
        self.game = game

    def register_player(self, member):
        if self.game.max_number_of_players < len(self._turn_manager.avatar_list):
            raise ValueError('this game game {self.game} already have max players')
        self._turn_manager.register_player(member)

    def start(self):
        if self._turn_manager.is_started:
            raise TypeError('game is already started')
        diff = self.game.min_number_of_players > len(self._turn_manager.avatar_list)
        if diff:
            raise ValueError(f'need more {diff} players')
        self._turn_manager.start()
        self.game.start(self._turn_manager)

    def play(self, member, action):
        if not self._turn_manager.is_started:
            raise ValueError('game is not started')
        current_turn_player = self._turn_manager.get_current_turn_player()
        if member != current_turn_player:
            raise ValueError(f'current turn player is {current_turn_player} not {player}')
        return self.game.play(self._turn_manager, action)

