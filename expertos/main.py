#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
import sys
import tomllib
from fastapi import FastAPI, Response, status
from expert import Expert
from openai import ChatGPT
from telegram import Telegram

FORMAT = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
logging.basicConfig(stream=sys.stdout, format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)


experts = {}
with open("config.toml", mode="r") as fr:
    content = fr.read()
    data = tomllib.loads(content)
    logger.debug(data)
    for data_expert in data["experts"]:
        experts[data_expert["name"]] = Expert(data_expert)
chat_gpt = ChatGPT(
    data["openai"]["url"],
    data["openai"]["endpoint"],
    data["openai"]["token"],
    data["openai"]["model"],
)
telegram = Telegram(data["telegram"]["url"], data["telegram"]["token"])

app = FastAPI()


@app.get("/status")
async def status_handler():
    logger.info("status_handler")
    return {"status": "Ok", "message": "up and running"}


@app.get("/query/{expert_name}")
@app.get("/query")
async def query_handler(response: Response, expert_name: str | None = None):
    experts_name = list(experts.keys())
    if expert_name:
        if expert_name in experts_name:
            expert = experts[expert_name]
            advice = await chat_gpt.post(expert)
            return {"status": "Ok", "advice": advice}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"status": "Ko",
                    "message": f"{expert_name} not found"}
    else:
        logger.debug(experts_name)
        return {"status": "Ok", "data": {"experts": experts_name}}


@app.get("/post/{expert_name}")
async def post_handler(expert_name: str, response: Response):
    try:
        experts_name = list(experts.keys())
        if expert_name:
            if expert_name in experts_name:
                expert = experts[expert_name]
                advice = await chat_gpt.post(expert)
                response = await telegram.post(expert, advice)
                logger.debug(response)
                return response
            else:
                response.status_code = status.HTTP_404_NOT_FOUND
                return {"status": "Ko",
                        "message": f"{expert_name} not found"}
        else:
            logger.debug(experts_name)
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"status": "Ko",
                    "message": "expert_name is mandatory"}
    except Exception as exception:
        logger.error(f"Error: {exception}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "Ko", "message": f"Error: {exception}"}
