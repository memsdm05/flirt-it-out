from quart import Quart, websocket, request
from .room import Room
from .host import Host

app = Quart(__name__)
room = Room()

@app.get("/")
async def index():
    return "hello world"

@app.get("/status")
async def status():
    return {
        "all": "good"
    }

@app.get("/register")
async def register_page():
    pass

@app.post("/register")
async def register_session():
    pass

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