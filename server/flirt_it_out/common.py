from collections import namedtuple
import configparser
from typing import Any
import asyncio
from quart import websocket
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .room import Room
else:
    Room = None

config = configparser.ConfigParser()

Message = namedtuple("Message", "id sender content")

def find(predicate, lst):
    return next(x for x in lst if predicate(x))

class Packet:
    pass

class PacketAgent:
    def __init__(self) -> None:
        self.outbox = asyncio.Queue()
        self.handlers = {}
    
    async def _consumer(self):
        while True:
            msg = await websocket.receive_json()
            pass

    async def _producer(self):
        while True:
            pass

    async def start(room: Room):
        pass