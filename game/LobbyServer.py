import logging
import uuid

from game.Lobby import Lobby
from game.Player import Player
from game.Response import Response


class LobbyServer:
    """handles all lobbies"""

    players_lobbies: dict[Player, Lobby] = {}

    id_lobbies: dict[str, Lobby] = {}

    def new_lobby(self, player: Player) -> Response | None:

        id = str(uuid.uuid4())
        lobby = Lobby(host=player, id=id)

        self.id_lobbies[id] = lobby

        return self.join_lobby(lobby=lobby, player=player)

    def delete_lobby(self) -> None:
        raise Exception(NotImplemented)

    def join_lobby(
        self,
        player: Player,
        id: str | None = None,
        lobby: Lobby | None = None,
    ) -> Response | None:

        if player in self.players_lobbies.keys():
            self.players_lobbies[player].leave(player)
            self.leave_lobby(player)

        if id:
            lobby = self.id_lobbies.get(id)

        if not lobby:
            logging.warning("lobby with that id not found")
            return None

        # if player in lobby.players:
        #     logging.warning("player already in lobby doing nothing")
        #     return None

        self.players_lobbies[player] = lobby

        lobby.join(player)

        if lobby.game:
            return lobby.game.join(player)
        return None

    def leave_lobby(self, player: Player) -> None:
        lobby = self.players_lobbies.get(player)
        if lobby and player not in lobby.players:
            logging.warning("player not in lobby doing nothing")
            return
        if lobby:
            lobby.leave(player)
            del self.players_lobbies[player]
