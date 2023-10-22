from typing import Any
import asyncio
from enum import Enum, auto

from .common import config
from .user import User

class RoomState(Enum):
    NONE = auto()
    LOBBY = auto()
    GAME = auto()
    LEADERBOARD = auto()
    END = auto()

class Chat:
    pass

class Room:
    def __init__(self) -> None:
        self.users = set()
        self.host = None
        
        # TODO maybe change this idk lol
        self.lobby_queue = asyncio.Queue()

        # associates userids with chats
        self.chats = {}

        self.current_state = RoomState.NONE

    async def create_user(self, name):
        user = User(name, self)
        self.users.add(user)
        return user

    async def create_host(self):
        pass

    async def start_round(self):
        pass

    async def end_round(self):
        pass