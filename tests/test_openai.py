#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import aiofiles
import tomllib
from expertos.openai import ChatGPT
from expertos.expert import Expert
import pytest

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_simple():
    await asyncio.sleep(0.5)


@pytest.mark.asyncio
async def test_loaddata():
    async with aiofiles.open("config.toml", mode="r") as fr:
        contents = await fr.read()
        data = tomllib.loads(contents)
        print(data)
    assert data is not None


@pytest.mark.asyncio
async def test_chatgpt():
    async with aiofiles.open("config.toml", mode="r") as fr:
        contents = await fr.read()
        data = tomllib.loads(contents)

    url = data["openai"]["url"]
    endpoint = data["openai"]["endpoint"]
    token = data["openai"]["token"]
    model = data["openai"]["model"]
    experts = {}
    for data_expert in data["experts"]:
        experts[data_expert["name"]] = Expert(data_expert)

    chat_gpt = ChatGPT(url, endpoint, token, model)
    response = await chat_gpt.post(experts["shell"])
    assert response is not None
    assert response != ""
