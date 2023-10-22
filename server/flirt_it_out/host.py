from .common import PacketAgent, ZERO_UUID, RoomState

class Host(PacketAgent):
    def __init__(self) -> None:
        super().__init__(ZERO_UUID)
        self.handlers = {
            "start_game": self.handle_start_game,
            "anim_end": self.handle_anim_end
        }

    async def handle_start_game(self, room, packet):
        room.state = RoomState.GAME

    async def handle_anim_end(self, room):
        pass