from .ai import Model
import asyncio
import uuid
import csv

class Bot:
    def __init__(self):
        self.model = Model()
        # add_user
        #
        self.personalities = self.read_csv('/home/ethan/flirt-it-out/server/flirt_it_out/ai/personalities.csv')

    def read_csv(self, path):
        with open(path, mode='r') as file:
            reader = csv.reader(file)
            return {rows[0]: rows[1] for rows in reader}

    async def send_message(self, msg: str):
        resp = await asyncio.to_thread(self.model.send_message(msg))
        return resp
    
    async def rate_chats(self, user_id: uuid.UUID):
        resp = await asyncio.to_thread(self.model.rate_chat(user_id))