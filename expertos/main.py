#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import aiofiles
import logging
import sys
import tomllib
from sanic import Sanic
from sanic.response import json
from sanic.request import Request
from expert import Expert
from openai import ChatGPT
from telegram import Telegram

FORMAT = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
logging.basicConfig(stream=sys.stdout, format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Sanic(__name__)


@app.before_server_start
async def attach_db(app, _):
    experts = {}
    async with aiofiles.open("config.toml", mode="r") as fr:
        contents = await fr.read()
        data = tomllib.loads(contents)
        logger.debug(data)
        for data_expert in data["experts"]:
            experts[data_expert["name"]] = Expert(data_expert)
    app.ctx.experts = experts
    app.ctx.chat_gpt = ChatGPT(
        data["openai"]["url"],
        data["openai"]["endpoint"],
        data["openai"]["token"],
        data["openai"]["model"],
    )
    app.ctx.telegram = Telegram(
        data["telegram"]["url"], data["telegram"]["token"])


@app.get("/status")
async def status_handler(_: Request):
    logger.info("status_handler")
    return json({"status": "Ok", "message": "up and running"})


@app.get("/query/<expert_name>", name="query_expert_name")
@app.get("/query")
async def query_handler(_: Request, expert_name: str | None = None):
    experts_name = list(app.ctx.experts.keys())
    if expert_name:
        if expert_name in experts_name:
            expert = app.ctx.experts[expert_name]
            response = await app.ctx.chat_gpt.post(expert)
            return json({"status": "Ok", "advice": response})
        else:
            return json({"status": "Ko",
                         "message": f"{expert_name} not found"})
    else:
        logger.debug(experts_name)
        return json({"status": "Ok", "data": {"experts": experts_name}})


@app.get("/post/<expert_name>", name="post_expert_name")
async def post_handler(_: Request, expert_name: str):
    try:
        experts_name = list(app.ctx.experts.keys())
        if expert_name:
            if expert_name in experts_name:
                expert = app.ctx.experts[expert_name]
                advice = await app.ctx.chat_gpt.post(expert)
                response = await app.ctx.telegram.post(expert, advice)
                logger.debug(response)
                return json(response)
            else:
                return json(
                    {"status": "Ko",
                     "message": f"{expert_name} not found"}, 404
                )
        else:
            logger.debug(experts_name)
            return json({"status": "Ko",
                         "message": "expert_name is mandatory"}, 400)
    except Exception as exception:
        logger.error(f"Error: {exception}")
        return json({"status": "Ko", "message": f"Error: {exception}"}, 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
