from __future__ import annotations
import asyncio
from threading import Thread
import random
import requests

from game.ConnectionManager import manager
from game.Player import Player
from game.Response import Random

from datetime import datetime


from typing import List, TypedDict


class Response(TypedDict):
    start: int
    end: int
    count: int
    type: str
    pageSize: int
    page: int
    pages: int
    columns: List[Column]
    items: List[Item]
    list: str
    miniList: str


class Column(TypedDict):
    label: str
    property: str
    sortable: bool


class Item(TypedDict):
    harmonic: str


class RandomQuery:
    @staticmethod
    def execute(player: Player):
        date = datetime.today().strftime('%Y/%m/%d')
        random_number = random.randint(1, 1000)
        r = requests.get(
            f"http://wikirank-2022.di.unimi.it/Q/?filter%5Btext%5D=Harmonic+centrality&filter%5Bselected%5D=true&filter%5Bvalue%5D=harmonic&view=list&pageSize=10&pageIndex={random_number}&type=harmonic&score=false"
        )
        data: Response = r.json()
        print(data)

        if r.status_code == 200:
            thread = Thread(
                target=asyncio.run,
                args=(manager.send_response(
                    Random(data=[article["harmonic"].split(">")[1].split("<")[0] for article in data["items"]], _recipients=[player])),),
            )
            thread.start()
        else:
            raise Exception("Error while fetching data from wikipedia search")
