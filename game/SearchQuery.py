import asyncio
from threading import Thread

import requests

from game.ConnectionManager import manager
from game.Player import Player
from game.Response import Wiki

# from collections import defaultdict


class SearchQuery:
    @staticmethod
    def execute(player: Player, query: str):
        r = requests.get(
            f"https://en.wikipedia.org/w/api.php?action=opensearch&search={query}&limit=10&namespace=0&format=json"
        )
        data = r.json()

        thread = Thread(
            target=asyncio.run,
            args=(manager.send_response(
                Wiki(data=data, _recipients=[player])),),
        )
        thread.start()
