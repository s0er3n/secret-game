import asyncio
import logging
from collections import defaultdict
from threading import Thread
from time import sleep
import uuid
import json

from game.Article import Article
from game.ConnectionManager import manager
from game.Game import Game
from game.GameState import State
from game.Player import Player, PlayerCopy
from game.PlayerData import PlayerData, PlayerRights, PlayerState, Node
from game.Query import Query
from game.Response import Error, LobbyUpdate, Response

logging.getLogger().setLevel(logging.INFO)


class SearchGame(Game):
    """handles all the game related stuff"""

    state: State = State.idle

    points: dict[Player, int]

    players: dict[Player, PlayerData]

    old_data: dict[Player, PlayerData]

    articles_to_find: set[Article]

    found_articles: set[Article]

    start_article: Article

    host: Player

    # TODO: why is here the id shouldnt it be in lobby server
    id: str

    play_time: int
    round: int = 0

    def __init__(self, id, host):
        self.points = defaultdict(int)
        self.players = {}
        self.old_data = {}
        self.id = id
        self.articles_to_find = set()
        self.found_articles = set()
        self.start_article = Article("", "")
        self.play_time = 60 * 10
        self.host = host

    def set_time(self, player: Player, time: int):
        if self._check_host(player):
            self.play_time = time
            return self._make_lobby_update_response()

    def join(self, player: Player) -> Response:
        if player in self.old_data.keys():
            # sending the starting postion to the player that joined
            self.players[player] = self.old_data.pop(player)
            if self.state == State.ingame:
                Query.execute(
                    move=self.players[player].moves[-1].url_name, recipient=player
                )
            return self._make_lobby_update_response()

        if player == self.host:
            self.players[player] = PlayerData(
                rights=PlayerRights.host,
            )
        else:
            self.players[player] = PlayerData(
                rights=PlayerRights.normal,
            )

        logging.info(f"joining player: {player}")
        return self._make_lobby_update_response()

    def leave(self, player: Player) -> Response:
        if player in self.players.keys():
            self.old_data[player] = self.players.pop(player)
            return self._make_lobby_update_response()

        # TODO: improve errors
        return Error(
            e="you are not in this lobby",
            _recipients=[player],
        )

    def _check_host(self, host: Player):
        logging.warning("no admin rights")
        return self.players[host].rights == PlayerRights.host

    def start(self, host: Player):
        if not self._check_host(host):
            return

        if not self.start_article:
            return

        if self.players[host].rights != PlayerRights.host:
            logging.warning("not allowed to start the game")
            return

        self.found_articles: set[Article] = set()
        self.round += 1
        self.state = State.ingame
        self._round_timer()
        self.set_starting_position()
        for player_data in self.players.values():
            player_data.state = PlayerState.hunting

        return self._make_lobby_update_response()

    def go_to_lobby(self, host: Player):
        if not self._check_host(host):
            return

        self.state = State.idle
        self.articles_to_find = set()

        for player_data in self.players.values():
            player_data.moves = []

        self.start_article = Article()

        return self._make_lobby_update_response()

    def _round_timer(self):
        async def update_state(round: int):
            sleep(self.play_time)
            if not (self.state == State.ingame and round == self.round):
                return
            self.state = State.over
            update_response = self._make_lobby_update_response()
            await manager.send_response(update_response)

        thread = Thread(target=asyncio.run, args=(
            update_state(round=self.round),))
        thread.start()

    def set_role(self, host: Player, player_id: str, role: str):
        player = next(
            player for player in self.players if player.id == player_id)

        role = PlayerState(role)
        if not self._check_host(host):
            return
        if not State.idle:
            logging.warning(
                "someone tried to change the role while ingame/gameover")
            return

        if not (role == PlayerState.hunting or role == PlayerState.watching):
            logging.warning("cannot give you that role")
            return

        self.players[player].state = role

        return self._make_lobby_update_response()

    def set_starting_position(self):
        """gets a random wiki page to start"""
        print("setting start position")
        print(self.players.values())

        for data in self.players.values():
            data.moves.clear()
            data.moves.append(self.start_article)

        for data in self.old_data.values():
            data.moves.clear()
            data.moves.append(self.start_article)

        for player in self.players:
            Query.execute(move=self.start_article.url_name, recipient=player)

    def _make_lobby_update_response(self) -> LobbyUpdate:
        logging.info(
            f"id: {self.id}, state: {self.state}, time: {self.play_time}, players: {self.players}")
        return LobbyUpdate(
            articles_to_find=list(
                article.pretty_name for article in self.articles_to_find
            ),
            articles_found=list(
                article.pretty_name for article in self.found_articles),
            start_article=self.start_article.pretty_name,
            id=self.id,
            state=self.state.value,
            time=self.play_time,
            players=[
                (
                    PlayerCopy(
                        id=player.id, name=player.name, points=self.points[player]
                    ),
                    playerData,
                )
                for player, playerData in self.players.items()
            ],
            _recipients=list(self.players.keys()),
        )

    def set_article(self, player: Player, article: str, better_name, start=False):

        if start:
            self.start_article = Article(
                url_name=article, pretty_name=better_name)
            self.players[player].nodes.append(Node(
                id=str(uuid.uuid4()),
                parent="",
                article=self.start_article
            ))
        else:
            self.articles_to_find.add(
                Article(url_name=article, pretty_name=better_name)
            )

        return self._make_lobby_update_response()

    def move(self, player: Player, url_name: str) -> Response:
        """when you click on a new link in wikipedia and move to the next page"""

        logging.info("move to " + url_name)
        if self.state != State.ingame:
            logging.warning("not allowed to move because not ingame")
            return Error(
                e="not allowed to move",
                _recipients=[player],
            )

        # if (
        #     self.players[player].state == PlayerState.watching
        #     or self.players[player].state == PlayerState.finnished
        # ):
        #     logging.warning("Watching People cannot not move")
        #     return Error(
        #         e="Watching People cannot not move",
        #         _recipients=[player],
        #     )

        if not self._is_move_allowed(url_name=url_name, player=player):
            logging.warning("cheate detected")
            return Error(
                e="cheater detected",
                _recipients=[player],
            )

        pretty_name = Query.execute(move=url_name, recipient=player)

        article = Article(pretty_name=pretty_name, url_name=url_name)

        self._add_points_current_move(article, player)

        self.players[player].moves.append(article)

        parent_node = self.players[player].nodes[-1]

        self.players[player].nodes.append(Node(
            id=str(uuid.uuid4()),
            article=article,
            parent=parent_node.id,
            children=list[Node],
        ))
        parent_node.children.append(self.players[player].nodes[-1].id)

        if self._check_if_player_found_all(player):
            self.state = State.over

        return self._make_lobby_update_response()

    def _is_move_allowed(self, url_name: str, player: Player):
        current_location = self.players[player].moves[-1].url_name
        # WARNING pretty confusing WARNING
        return url_name in Query.queries[current_location]["links"]

    def _add_points_current_move(self, target: Article, player: Player):
        if target not in self.articles_to_find:
            logging.info("move not in articles to find")
            return
        if target in self.players[player].moves:
            logging.info(
                "article already found by player not counting it again")
            return

        if target in self.found_articles:
            logging.info("article found but not first")
            self.points[player] += 10
            return

        logging.info("article found for the first time")
        self.points[player] += 15

        self.found_articles.add(target)

    def _check_if_player_found_all(self, player: Player):
        if player_data := self.players.get(player):
            return set(player_data.moves).issuperset(self.articles_to_find)
