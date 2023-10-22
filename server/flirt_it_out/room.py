from typing import Any
import asyncio
from enum import Enum, auto
import uuid

from .common import config, ZERO_UUID
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
        self.users: dict[uuid.UUID, User] = {}
        self.host: Host | None = None
        
        # TODO maybe change this idk lol
        self.lobby_queue = asyncio.Queue()

        # associates userids with chats
        self.chats = {}

        self.current_state = RoomState.NONE

    async def create_user(self, name):
        user = User(name)
        await user.send("hello")
        self.users[user.id] = user
        return user
    
    async def create_host(self):
        pass
    
    def find_user(self, uuid_str):
        try:
            uid = uuid.UUID(uuid_str)
        except:
            return None
        
        if uid not in self.users:
            return None
        
        return self.users[uid]
    
    async def broadcast(self, packet, *, host=False):
        if host:
            await self.host.send(packet)

        for user in self.users.values():
            await user.send(packet)

    async def kick(self, agent):
        uid = agent.id

        if uid == ZERO_UUID:
            await self.host.disconnect()
            self.host = None

        if uid in self.users:
             await self.users[uid].disconnect()
             del self.users[uid]

        print("kick", self.host, self.users)

    async def start_round(self):
        pass

    async def end_round(self):
        pass