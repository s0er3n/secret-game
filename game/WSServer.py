
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
import logging

from game.ConnectionManager import manager
from game.LobbyServer import LobbyServer
from game.Response import Error, Response
from game.SearchGame import Player, SearchGame
from game.SearchQuery import SearchQuery

app = FastAPI()


lobbyServer = LobbyServer()


@app.get("/")
def index():
    return "hallo"


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    player = await manager.connect(websocket, id=client_id)
    try:
        while True:
            data = await websocket.receive_json()
            logging.info("data received by backend: "+data)

            match data:

                case {
                    "type": "game" | "lobby" | "player" | "search",
                    "method": method,
                    "args": args,
                }:
                    if method.startswith("_"):
                        raise Exception("not allowed")

                    if data.get("type") == "player":
                        target: SearchQuery | SearchGame | LobbyServer | Player = player
                    elif data.get("type") == "game":
                        lobby = lobbyServer.players_lobbies.get(player)
                        if lobby and (game := lobby.game):
                            target = game
                    elif data.get("type") == "search":
                        target = SearchQuery()
                    else:
                        target = lobbyServer
                    await manager.send_response(getattr(target, method)(player, **args))

                case _:
                    await manager.send_response(
                        message=Error(
                            _recipients=[player],
                            e="not matching anything",
                        )
                    )

            #     await manager.send_personal_message(
            #         asdict(lobbyServer.new_lobby(player)), player)
            # else:

    except WebSocketDisconnect:
        manager.disconnect(player)
