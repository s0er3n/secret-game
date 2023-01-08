import dataclasses

user_names = {}


@dataclasses.dataclass(frozen=True)
class Player:

    id: str

    @property
    def name(self):
        return user_names.get(self.id) or "unnamed"

    def set_name(self, name: str):
        user_names[self.id] = name

    @staticmethod
    def set_user_name(player, name: str):
        player.set_name(name)


@dataclasses.dataclass
class PlayerCopy:
    id: str
    name: str
    points: int
