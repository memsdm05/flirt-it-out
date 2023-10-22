from quart import (
    Quart,
    websocket,
    request,
    session,
    render_template,
    abort,
    url_for,
    redirect,
)
from quart_cors import cors

from .room import Room
from .host import Host
from .common import config, find

import aiofiles

app = Quart(__name__)
app = cors(app)
room = None

@app.before_serving
async def setup():
    global room

    async with aiofiles.open("config.ini", "r") as f:
        text = await f.read()
        config.read_string(text)
    print(f"loaded config: {config.sections()}")

    room = Room()

    app.config["SECRET_KEY"] = config["server"]["secret_key"]


@app.after_serving
async def shutdown():
    pass


@app.before_request
async def pre_request():
    session.permanent = True


@app.get("/")
async def index():
    if "uid" not in session:
        return redirect("/register")

    return "hello world"


@app.get("/status")
async def status():
    return {"all": "good"}


@app.get("/register")
async def register_page():
    return await render_template("register.html")


@app.post("/register")
async def register_session():
    form = await request.form
    name = form.get("name")

    if not name:
        return abort(402)

    # if find(room.users, lambda user: user.name == name):
    #     # TODO maybe only check if user session has what it needs
    #     return f"user {name} already exists"

    if session.get("name") != name:
        session.clear()

    if "uid" in session:
        return redirect("/")

    user = await room.create_user(name)
    session["uid"] = str(user.id)
    session["name"] = name

    return redirect("/")


@app.websocket("/client")
async def client_stream():
    pass


@app.websocket("/host")
async def host_stream():
    pass


@app.websocket("/echo")
async def test_echo():
    await websocket.send("hello world")
    while True:
        data = await websocket.receive()
        print(f"got: {data}")
        await websocket.send(data)
