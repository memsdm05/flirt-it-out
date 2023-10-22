from typing import Any
import asyncio
from enum import Enum, auto

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

        self.current_state = RoomState.NONE

    async def create_user(name):
        pass

    async def create_host():
        pass

    async def start_round():
        pass

    async def end_round():
        pass