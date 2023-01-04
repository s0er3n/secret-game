import dataclasses
from enum import Enum
import uuid

from game.Article import Article


class PlayerRights(str, Enum):
    host = "host"
    normal = "normal"


class PlayerState(str, Enum):
    hunting = "hunting"
    watching = "watching"
    finnished = "finnished"


@dataclasses.dataclass
class Node:
    id: str
    article: Article
    parent: str
    children: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class PlayerData:
    rights: PlayerRights

    state: PlayerState = PlayerState.watching

    moves: list[Article] = dataclasses.field(default_factory=list)

    node_position: str = ""

    nodes: list[Node] = dataclasses.field(default_factory=list)
