from quart import (
    Quart,
    websocket,
    request,
    session,
    render_template,
    abort,
    url_for,
    redirect,
    send_from_directory,
)
from quart_cors import cors
import json
import uuid

from .room import Room
from .host import Host
from .common import config, Packet
from .user import User

import aiofiles

app = Quart(__name__)
# app = cors(app)
room = None

class MoneyJSONEncoder(json.JSONEncoder):
    def default(self, object_):
        if isinstance(object_, uuid.UUID):
            return str(object_)
        elif isinstance(object_, Packet):
            packet: Packet = object_
            return {
                "action": packet.action,
                "payload": "_" + json.dumps(packet.payload)
            }
        else:
            return super().default(object_)

class MoneyJSONDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.dict_to_object, *args, **kwargs)

    def dict_to_object(self, dict_):
        if "id" in dict_:
            return uuid.UUID(dict_["id"])
        else:
            return dict_

app.json_decoder = MoneyJSONDecoder
app.json_encoder = MoneyJSONEncoder


@app.before_serving
async def setup():
    global room

    async with aiofiles.open("config.ini", "r") as f:
        text = await f.read()
        config.read_string(text)
    print(f"loaded config: {config.sections()}")

    room = Room(
        duration=int(config["round"]["length"])
    )

    app.config["SECRET_KEY"] = config["server"]["secret_key"]

    await room.start()


@app.after_serving
async def shutdown():
    # await room.end()
    raise Exception("STOP")


@app.before_request
async def pre_request():
    session.permanent = True

@app.route("/_app/immutable/<path:path>")
async def serve_stuff(path):
    return await send_from_directory('../web/build/_app/immutable', path)

@app.get("/")
async def index():
    if "uid" not in session:
        return redirect("/register")
    
    return await send_from_directory("../web/build", "index.html")


@app.get("/status")
async def status():
    return {"all": "good"}


@app.get("/register")
async def register_page():
    return await send_from_directory("../web/build/register", "index.html")


@app.post("/register")
async def register_session():
    form = await request.form
    name = form.get("name")
    
    if not name:
        return abort(402)

    if session.get("name") != name:
        session.clear()

    user = await room.create_user(name)
    session["uid"] = str(user.id)
    session["name"] = name

    return redirect("/")


@app.websocket("/client")
async def client_stream():
    uuid_str = session.get("uid")
    print(session)
    if not uuid_str:
        print("shit")
        abort(500)

    user: User = room.find_user(uuid_str)
    if not user:
        abort(501)

    await websocket.accept()
    return await user.start(room)
    

@app.websocket("/host")
async def host_stream():
    await websocket.accept()

    if room.host:
        abort(403)

    host = await room.create_host()

    await websocket.accept()
    return await host.start(room)

@app.websocket("/echo")
async def test_echo():
    await websocket.send("hello world")
    while True:
        data = await websocket.receive()
        print(f"got: {data}")
        await websocket.send(data)
