from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from parlai.core.agents import create_agent

import logging

logging.basicConfig(filename='message.log', level=logging.INFO)
logger = logging.getLogger(__name__)


blender = {
    'model_file': 'zoo:blender/blender_90M/model',
    'model': 'transformer/generator',
}

agent = create_agent(blender)


app = FastAPI()


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


class Message(BaseModel):
    text: str


@app.post("/")
async def respond(message: Message):
    agent.observe({"text": message.text, "episode_done": True})
    agent_act = agent.act()
    logger.info(f"Replied user message {message.text}")

    return JSONResponse({"text": agent_act['text']})