import asyncio
import logging
from threading import Thread
from typing import Iterator

import requests
from bs4 import BeautifulSoup

from game.Player import Player
from game.Response import Wiki
from game.QueryResult import QueryResult
from game.ConnectionManager import manager


def _select_and_reduce_links(all_links) -> Iterator[str]:
    for link in all_links:
        if link["href"].startswith("/wiki/") and not link["href"].startswith("/wiki/Help") and not link["href"].startswith("/wiki/File"):
            yield link["href"][6::]


class Query:
    # i will query one by one for MVP
    # next_query: dict[str, list[Player]] = defaultdict(list)

    queries: dict[str, QueryResult] = dict()

    @classmethod
    def _query_and_add_to_queries(cls, move: str) -> None:
        logging.warning(f"add move to query {move}")
        resp_text = requests.get(
            f"https://en.wikipedia.org/wiki/{move}"
        ).text

        soup = BeautifulSoup(resp_text, "html.parser")

        if not (h1 := soup.find("h1")):
            logging.warning("no h1")
            return None
        title = h1.text

        article = soup.find("div", {"id": "mw-content-text"})

        # data = _skip_if_redirect(data)

        all_links = soup.find_all("a", href=True)

        short_links = list(_select_and_reduce_links(all_links))

        if len(cls.queries) > 500:
            cls.queries.clear()
        cls.queries[move] = {"links": short_links,
                             "title": str(title),
                             "content_html": str(article),
                             "url_ending": move}

    @classmethod
    def execute(cls, move: str, recipient: Player) -> str | None:
        if not cls.queries.get(move):
            logging.warning(f"before try move {move}")
            try:
                cls._query_and_add_to_queries(move)
            except:
                logging.error("could not query wikipedia")
                return

        if not (query_result := cls.queries.get(move)):
            logging.warning("no query result")
            return None
        thread = Thread(
            target=asyncio.run,
            args=(
                manager.send_response(
                    Wiki(
                        data=query_result,
                        _recipients=[recipient],
                    )
                ),
            ),
        )
        thread.start()
        return query_result["title"]


def test_query() -> None:
    target = "berlin"
    Query._query_and_add_to_queries(target)
    assert Query.queries.get(target) is not None
