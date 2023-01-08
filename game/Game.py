from game.Player import Player
from game.Response import Response

# base class for different game modes


class Game:
    host: Player

    def leave(self, player: Player) -> Response:
        raise Exception(NotImplemented)

    def join(self, player: Player) -> Response:
        raise Exception(NotImplemented)
