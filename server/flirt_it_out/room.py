from typing import Any
import asyncio
from enum import Enum, auto
import uuid

from .common import config
from .user import User
from .host import Host

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
        self.users: set[User] = set()
        self.host: Host | None = None
        
        # TODO maybe change this idk lol
        self.lobby_queue = asyncio.Queue()

        # associates userids with chats
        self.chats = {}

        self.current_state = RoomState.NONE

    async def create_user(self, name):
        user = User(name, self)
        self.users.add(user)
        return user
    
    def find_user(self, uuid_str):
        try:
            uid = uuid.UUID(uuid_str)
        except:
            return None
        
        for user in self.users:
            if user.id == uid:
                return user
        return None
    
    async def create_host(self):
        pass

    async def kick(self, agent):
        if agent == self.host:
            await self.host.disconnect()
            self.host = None
        

        for user in self.users:
            if agent == user:
                await user.disconnect()
                self.users.remove(user)
                break

    async def start_round(self):
        pass

    async def end_round(self):
        pass