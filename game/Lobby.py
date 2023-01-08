from game.Player import Player
from game.SearchGame import SearchGame


class Lobby:
    players: list[Player]
    game: SearchGame | None
    host: Player

    def __init__(self, host: Player, id: str, Game=SearchGame) -> None:
        self.host = host
        self.players = []
        self.game = Game(host=host, id=id)

    def leave(self, player) -> None:
        if isinstance(self.game, SearchGame):
            self.game.leave(player)
        if player in self.players:
            self.players.remove(player)

    def join(self, player) -> None:
        self.players.append(player)
