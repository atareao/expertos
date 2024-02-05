#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import aiofiles
import tomllib
from expertos.telegram import Telegram
from expertos.expert import Expert
import pytest

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_telegram():
    async with aiofiles.open("config.toml", mode="r") as fr:
        contents = await fr.read()
        data = tomllib.loads(contents)

    url = data["telegram"]["url"]
    token = data["telegram"]["token"]
    telegram = Telegram(url, token)
    experts = {}
    for data_expert in data["experts"]:
        experts[data_expert["name"]] = Expert(data_expert)

    response = await telegram.post(experts["shell"], "Hola!")
    assert response is not None
    assert response != ""
