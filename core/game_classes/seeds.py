class Seed:
    _user_text = None
    _game_value = None

    def __init__(self, game_value, user_seed=None):
        self._game_value = game_value
        self._user_text = user_seed or game_value

    @property
    def input_value(self):
        return self._user_text or self._game_value

    @property
    def game_value(self):
        return self._game_value
