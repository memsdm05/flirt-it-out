from collections import namedtuple
from dataclasses import dataclass, field
import configparser
from typing import Any
import asyncio
from quart import websocket
import uuid
from typing import TYPE_CHECKING
from enum import Enum, auto

if TYPE_CHECKING:
    from .room import Room
else:
    Room = None

ZERO_UUID = uuid.UUID(int=0)
config = configparser.ConfigParser()

class RoomState(Enum):
    NONE = auto()
    LOBBY = auto()
    GAME = auto()
    SCORES = auto()
    LEADERBOARD = auto()
    END = auto()

Message = namedtuple("Message", "sender content")

@dataclass
class Packet:
    action: str
    payload: dict = field(default_factory=dict)


class PacketAgent:
    def __init__(self, uid) -> None:
        self.outbox = asyncio.Queue()
        self.handlers = None
        self.connected = False
        self.id = uid

        self.consumer = None
        self.producer = None

    async def _consumer(self, room):
        while True:
            data = await websocket.receive_json()
            if "payload" in data:
                packet = Packet(action=data["action"], payload=data["payload"])
            else:
                packet = Packet(action=data["action"])

            if not self.handlers:
                continue

            if packet.action not in self.handlers:
                continue
            
            handler = self.handlers[packet.action]

            await handler(room, packet)

    async def _producer(self, room: Room):
        try:
            while True:
                out = await self.outbox.get()
                await websocket.send_json(out)
        except asyncio.CancelledError:
            await room.kick(self)
            raise

    async def send(self, packet):
        await self.outbox.put(packet)

    async def start(self, room: Room):
        self.consumer = asyncio.ensure_future(self._consumer(room))
        self.producer = asyncio.ensure_future(self._producer(room))
        self.connected = True
        return await asyncio.gather(self.consumer, self.producer)
    
    async def disconnect(self):
        self.consumer.cancel()
        self.producer.cancel()

        # await self.consumer
        # await self.producer

        # lmao
        try:
            await websocket.close(1000, reason="disconnect")
        except:
            pass

        self.connected = False
