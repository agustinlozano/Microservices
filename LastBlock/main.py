# LastBlock
from fastapi import FastAPI
from pydantic import BaseModel
import websockets
import asyncio
import json

f = open('config.json')

config = json.load(f)

print(config['WS_PORT'])
print(config['WS_IP'])

WS_URL = f"{config['WS_IP']}:{config['WS_PORT']}"

print("WebSocket server is running on: ", WS_URL)

app = FastAPI()

class LastBlock(BaseModel):
    lastblock: str
    projectid: str

class Message(BaseModel):
    code: str
    projectid: str

async def sendWsData(lastblock, projectid):
    async with websockets.connect(WS_URL) as websocket:
        # send data (Message) to websocket
        await websocket.send(Message(code=lastblock, projectid=projectid).json())
        received = await websocket.recv()
        print(f"\nLB> Received: {received}")

@app.post("/lastblock")
def root(data: LastBlock):
    # send data to websocket
    asyncio.run(sendWsData(data.lastblock, data.projectid))

    # what the root function returns
    return {"message": f"You wrote: '{data.lastblock + '-' + data.projectid}'"}