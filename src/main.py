#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib
import logging
import os
import sys
import tomllib
from typing import Dict

from sanic import Sanic
from sanic.request import Request
from sanic.response import json

from db import DB
from openai import ChatGPT
from telegram import Telegram

FORMAT = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
logging.basicConfig(stream=sys.stdout, format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)


def instanciate(module_name: str,
                class_name: str,
                db: DB,
                data: Dict[str, str]) -> object:
    """Instanciate a class from a module."""
    module = importlib.import_module(module_name)
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
    """Get the status of the server

    Parameters
    ----------
    request : Request
        the request

    """
    logger.info("status_handler")
    return json({"status": "Ok", "message": "up and running"})


@app.get("/query")
async def query_handler(request: Request):
    """Ask for a new query

    openapi:
    ---
    parameters:
      - name: expert
        in: expert
        description: the name of the expert
        required: false
        schema:
          type: string
    responses:
      '200':
        description: the advice
      '200':
        description: the list of experts if no expert name is provided
      '404':
        description: not found
    """
    expert_names = list(app.ctx.experts.keys())
    logger.debug(expert_names)
    expert_name = request.args.get("expert")
    logger.debug(expert_name)
    if expert_name:
        if expert_name in expert_names:
            expert = app.ctx.experts[expert_name]
            dialog = expert.get_dialog()
            message = await app.ctx.chat_gpt.post(dialog)
            return json({"status": "Ok", "message": message})
        else:
            return json({"status": "Ko",
                         "message": f"{expert_name} not found"}, 404)
    else:
        logger.debug(expert_names)
        return json({"status": "Ok", "data": {"experts": expert_names}})


@app.get("/post")
async def post_handler(request: Request):
    """Post a new query in telegram

    openapi:
    ---
    parameters:
      - name: expert
        in: expert
        description: the name of the expert
        required: false
        schema:
        type: string
      - name: chat_id
        in: chat_id
        description: the chat_id of Telegram
        required: true
        schema:
          type: string
      - name: thread_id
        in: thread_id
        description: the thread_id of Telegram
        required: false
        schema:
          type: integer
          format: int32
    responses:
      '200':
        description: the response of Telegram
      '400':
        description: if chat_id is not provided
      '400':
        description: if expert is not provided
      '404':
        description: if expert is not found
      '500':
        description: another error
    """
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
                    dialog = expert.get_dialog()
                    message = await app.ctx.chat_gpt.post(dialog)
                    response = await app.ctx.telegram.postMarkdown(chat_id,
                        thread_id, message)
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
