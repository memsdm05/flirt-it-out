from typing import Any
import asyncio
import uuid
from datetime import timedelta, datetime

from .common import config, ZERO_UUID, Packet, Message, RoomState
from .user import User
from .host import Host


class Room:
    SCREW_HOST_I_DONT_NEED_IT = False

    def __init__(self, duration, rounds=0) -> None:
        self.users: dict[uuid.UUID, User] = {}
        self.host: Host | None = None

        self.game_loop = None

        # TODO maybe change this idk lol
        self.lobby_queue = asyncio.Queue()
        self.pending_messages = asyncio.Queue()

        self.duration = duration

        # associates userids with chats
        self.chats = {}
        self.end_round_alarm = None
        self.host_connected = asyncio.get_event_loop().create_future()
        self.state = RoomState.NONE

    async def start(self):
        self.game_loop = asyncio.ensure_future(self.loop())

    async def loop(self):
        if not self.SCREW_HOST_I_DONT_NEED_IT:
            await self.host_connected
        self.state = RoomState.LOBBY
        while True:
            if self.state == RoomState.LOBBY:
                while self.state == RoomState.LOBBY:
                    new_user = await self.lobby_queue.get()
                    self.users[new_user.id] = new_user
                await self.broadcast(Packet("start_game"))
            elif self.state == RoomState.GAME:
                while self.state == RoomState.GAME:
                    msg: Message = await self.pending_messages.get()
                    user = self.find_user(str(msg.sender.id))

                    print("thing", user)

                    if user:
                        if msg.content == "stasis":
                            await user.send(Packet("stasis", {"display": "stop doing shit"}))
                        else:
                            await user.send(Packet("msg", {"content": f"I see your '{msg.content}'"}))
            elif self.state == RoomState.END:
                if self.host:
                    await self.host.disconnect()
                for user in self.users.values():
                    await user.disconnect()

    async def start_game(self):
        pass
    
    async def end_game(self):
        pass

    async def end(self):
        self.game_loop.cancel()
        if self.host:
            await self.host.disconnect()
        for user in self.users.values():
            await user.disconnect()
        
    async def create_user(self, name):
        user = User(name)
        await user.send(Packet("hello"))
        await user.send(Packet("stasis", {"display": "waiting for start of game"}))
        self.lobby_queue.put(user)
        return user

    async def create_host(self):
        host = Host()
        await host.send(Packet("hello"))
        self.host = host
        self.host_connected.set_result(True)
        return host

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

    async def create_end_round_alarm(self):
        await asyncio.sleep(self.duration)
        await self.end_round()
    
    async def start_round(self):
        self.state = RoomState.GAME
        
        ends_at = datetime.now() + timedelta(seconds=self.duration)
        self.end_round_alarm = asyncio.ensure_future(self.create_end_round_alarm())

        self.broadcast(
            Packet("start_round", {"ends_at": ends_at.isoformat(), "bot_name": "jeff"}), 
            host=True
        )

    async def end_round(self):
        self.state = RoomState.SCORES
        self.broadcast(
            Packet("end_round"),
            host=True
        )

        # rating stuff here
