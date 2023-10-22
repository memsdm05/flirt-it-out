import uuid
from .common import PacketAgent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .room import Room
else:
    Room = None

class User(PacketAgent):
    def __init__(self, name: str, room: Room) -> None:
        self.id = uuid.uuid1()
        self.name = name
        self.room = room

    async def handle_so_and_so():
        pass