from __future__ import annotations

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
    article: Article
    parent: Node | None
    children: list[Node] = dataclasses.field(default_factory=list)

    def add_child(self, article: Article) -> Node:
        new_node = Node(
            article=article, parent=self
        )
        self.children.append(new_node)
        return new_node


@dataclasses.dataclass
class PlayerData:
    rights: PlayerRights
    state: PlayerState = PlayerState.watching
    moves: list[Article] = dataclasses.field(default_factory=list)
    node_position: Node | None = None
    nodes: list[Node] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class PlayerDataNoNode:
    rights: PlayerRights
    state: PlayerState = PlayerState.watching
    moves: list[Article] = dataclasses.field(default_factory=list)
