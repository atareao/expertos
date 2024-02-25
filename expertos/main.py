#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import importlib
import logging
import os
import sys
import tomllib
from typing import Dict, Union
from sanic import Sanic
from sanic import json
from sanic.request import Request
from expertos.db import DB
from expertos.openai import ChatGPT
from expertos.telegram import Telegram

FORMAT = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
logging.basicConfig(stream=sys.stdout, format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)


def instanciate(module_name: str,
                class_name: str,
                db: DB,
                data: Dict[str, str]) -> object:
    module = importlib.import_module(f"expertos.{module_name}")
    Klass = getattr(module, class_name)
    return Klass(db, data)


app = Sanic("Expertos")


@app.before_server_start
async def attach_db(app, loop):
    app.ctx.experts = {}
    app.ctx.db = DB("/app/expertos.db")
    with open("config.toml", mode="r") as fr:
        content = fr.read()
        data = tomllib.loads(content)
        logger.debug(data)
        for data_expert in data["experts"]:
            app.ctx.experts[data_expert["name"]] = instanciate(
                data_expert["module"],
                data_expert["class"],
                app.ctx.db,
                data_expert)
    app.ctx.chat_gpt = ChatGPT(
        data["openai"]["url"],
        data["openai"]["endpoint"],
        data["openai"]["token"],
        data["openai"]["model"],
    )
    app.ctx.telegram = Telegram(data["telegram"]["url"],
                                data["telegram"]["token"])


@app.get("/status")
async def status_handler(request: Request):
    logger.info("status_handler")
    return json({"status": "Ok", "message": "up and running"})


@app.get("/query")
async def query_handler(request: Request):
    expert_names = list(app.ctx.experts.keys())
    logger.debug(expert_names)
    expert_name = request.args.get("expert")
    logger.debug(expert_name)
    if expert_name:
        if expert_name in expert_names:
            expert = app.ctx.experts[expert_name]
            messages = expert.get_messages()
            advice = await app.ctx.chat_gpt.post(messages)
            return json({"status": "Ok", "advice": advice})
        else:
            return json({"status": "Ko",
                         "message": f"{expert_name} not found"}, 404)
    else:
        logger.debug(expert_names)
        return json({"status": "Ok", "data": {"experts": expert_names}})


@app.get("/post")
async def post_handler(request: Request):
    try:
        experts_name = list(app.ctx.experts.keys())
        expert_name = request.args.get("expert")
        chat_id = request.args.get("chat_id")
        thread_id = request.args.get("thread_id")
        logger.debug(f"chat_id: {chat_id}, thread_id: {thread_id}")
        if expert_name:
            if expert_name in experts_name:
                if chat_id:
                    thread_id = thread_id if thread_id else 0
                    expert = app.ctx.experts[expert_name]
                    message = await app.ctx.chat_gpt.post(expert)
                    response = await app.ctx.telegram.post(chat_id, thread_id,
                                                           message)
                    logger.debug(response)
                    return json(response)
                else:
                    return json({"status": "Ko",
                                 "message": "chat_id is mandatory"}, 400)
            else:
                return json({"status": "Ko",
                             "message": f"{expert_name} not found"}, 404)
        else:
            logger.debug(experts_name)
            return json({"status": "Ko",
                         "message": "expert_name is mandatory"}, 400)
    except Exception as exception:
        logger.error(f"Error: {exception}")
        return json({"status": "Ko", "message": f"Error: {exception}"}, 500)
