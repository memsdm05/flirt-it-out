from .ai import Model
import asyncio
import uuid

class Bot:
    def __init__(self):
        self.model = Model()
        # add_user
        #
        self.personalities = {}

    def read_personalities(self, path):
        with open(path) as f:
            for line in f.readlines():
                print(line)

    async def send_message(self, msg: str):
        resp = await asyncio.to_thread(self.model.send_message(msg))
        return resp
    
    async def rate_chats(self, user_id: uuid.UUID):
        resp = await asyncio.to_thread(self.model.rate_chat(user_id))