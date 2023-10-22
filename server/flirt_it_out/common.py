from collections import namedtuple
from dataclasses import dataclass, field
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


@dataclass
class Packet:
    action: str
    payload: dict = field(default_factory=dict)

    def __get__(self, thing: str) -> Any:
        return self.payload[thing]


class PacketAgent:
    def __init__(self) -> None:
        self.outbox = asyncio.Queue()
        self.handlers = None
        self.connected = False

        self.consumer = None
        self.producer = None

    async def _consumer(self, room):
        while True:
            data = await websocket.receive_json()
            packet = Packet(action=data["action"], payload=data["payload"])

            if not self.handlers:
                continue

            if packet.action not in self.handlers:
                continue

            await self.handlers[packet.action](room, **packet.payload)

    async def _producer(self, room: Room):
        try:
            while True:
                out = await self.outbox.get()
                await websocket.send_json(out)
        except:
            room.kick(self)
            self.disconnect()

    async def start(self, room: Room):
        await self.outbox.put(Packet("hello"))

        self.consumer = asyncio.create_task(self._consumer(room))
        self.producer = asyncio.create_task(self._producer(room))
        self.connected = True
        return await asyncio.gather(self.consumer, self.producer)
    
    async def disconnect(self):
        self.consumer.cancel()
        self.producer.cancel()

        await self.consumer
        await self.producer

        self.connected = False
