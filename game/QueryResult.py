
from typing import TypedDict


class QueryResult(TypedDict):
    links: list[str]
    title: str
    content_html: str
    url_ending: str
