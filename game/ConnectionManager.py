import logging
from dataclasses import asdict

from fastapi import WebSocket

from game.Player import Player
from game.Response import Response


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[Player, WebSocket] = {}
        self.players: dict[str, Player] = {}

    async def connect(self, websocket: WebSocket, id: str) -> Player:
        await websocket.accept()
        player = self.players.get(id)
        if not player:
            player = Player(id=id)
            self.players[id] = player

        self.active_connections[player] = websocket
        return player

    def disconnect(self, player: Player) -> None:
        del self.active_connections[player]

    async def send_response(self, message: Response | None) -> None:
        if not message:
            logging.warning("no response")
            return

        for player in message._recipients:
            try:
                message._recipients = []
                await self.active_connections[player].send_json(asdict(message))
            except Exception as e:
                print("couldnt send message ", e)


manager = ConnectionManager()
