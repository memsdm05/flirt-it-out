import uuid
from .common import PacketAgent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .room import Room
else:
    Room = None

class User(PacketAgent):
    def __init__(self, name: str, room: Room) -> None:
        super(User, self).__init__()

        self.id = uuid.uuid1()
        self.name = name
        self.room = room

        self.handlers = {
            "msg": self.handle_msg
        }

    async def handle_msg(self, room: Room, content):
        print(content)