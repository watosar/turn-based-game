"""
abc turn based game
"""


class Turn:
    def __init__(self, size=1):
        if size < 1:
            raise ValueError('size must be natural number, not', size)
        self._turn_count = 0
        self.circle_size = size

    @property
    def current_turn(self):
        return self._turn_count % self.circle_size

    def __next__(self):
        self._turn_count += 1


class TurnBasedGame:
    class Player:
        pass

    max_number_of_players = None
    min_number_of_players = None

    def __init__(self):
        if not isinstance(self.max_number_of_players, int) or not isinstance(self.min_number_of_players, int):
            raise NotImplementedError("needs to set int to {max_number_of_players} and {min_number_of_players} ")
        self.is_open = False
        self.is_end = False
        self.turn = None
        self.players = []

    def create_player(self) -> Player:
        if not len(self.players) < self.max_number_of_players:
            raise ValueError(f"max number of players is {self.max_number_of_players}")
        player = self.Player()
        self.players.append(player)
        return player

    @property
    def current_player(self) -> Player:
        return self.players[self.turn.current_turn]

    def init_game(self):
        if len(self.players) < self.min_number_of_players:
            raise ValueError(f"need at least of {self.min_number_of_players} players")
        self.turn = Turn(len(self.players))
        self.is_open = True

    def play(self, action):
        if self.is_end:
            raise ValueError('already ended')
        if not self.is_open:
            raise ValueError('game is not initialized')

        # some actions
        # next(self.turn)

    def __str__(self):
        return ''  # 最小限のstr


class Member:
    def __init__(self, **data):
        self.__dict__.update(data)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class MemberTurnManager:
    """
    Member Manager
    """

    def __init__(self, game):
        self.members = dict()
        self.game = game

    def register_member(self, member=None, **kwargs):
        if self.game.is_open:
            raise ValueError("game is already opened")

        player = self.game.create_player()
        if member is None:
            member = Member(**kwargs)
        self.members[player] = member

    @property
    def current_turn_member(self):
        return self.members[self.game.current_player]

    def _current_turn_member_is(self, member) -> bool:
        return member == self.current_turn_member

    def get_player(self, member):
        return next(p for p, m in self.members.items() if m == member)

    def play(self, member, action):
        print('play')
        if not self._current_turn_member_is(member):
            raise ValueError(f"current turn player is {self.current_turn_member} not {member}")
        print('send action')
        return self.game.play(action)


class GameManager:
    def __init__(self, game):
        self.game = game
        self.member_turn_manager = MemberTurnManager(self.game)

    def register_member(self, *args, **kwargs):
        self.member_turn_manager.register_member(*args, **kwargs)

    def get_current_turn_member(self):
        return self.member_turn_manager.current_turn_member

    def get_player(self, member):
        return self.member_turn_manager.get_player(member)

    def play(self, ):

