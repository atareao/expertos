#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from httpx import AsyncClient
from expert import Expert
from datetime import datetime

logger = logging.getLogger(__name__)


class ChatGPT:
    def __init__(self, url: str, endpoint, token: str, model: str):
        logger.info("__init__")
        self._url = f"https://{url}/{endpoint}"
        self._headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self._model = model

    async def post(self, expert: Expert, variables: dict) -> str:
        logger.info("post")
        payload = {
            "model": self._model,
            "messages": expert.messages(variables)
        }
        async with AsyncClient() as client:
            response = await client.post(
                self._url, headers=self._headers, json=payload
            )
            logger.debug(f"Response: {response}")
            if response.status_code == 200:
                data = response.json()
                response = data["choices"][0]["message"]["content"]
                return response
            else:
                msg = f"HTTP Error: {response.status_code}"
                raise Exception(msg)


async def main():
    import tomllib
    import aiofiles
    from pprint import pprint
    experts = {}

    async with aiofiles.open("config.toml", mode="r") as fr:
        contents = await fr.read()
        data = tomllib.loads(contents)
        pprint(data)
        for data_expert in data["experts"]:
            experts[data_expert["name"]] = Expert(data_expert)

    url = data["openai"]["url"]
    endpoint = data["openai"]["endpoint"]
    token = data["openai"]["token"]
    model = data["openai"]["model"]

    chat_gpt = ChatGPT(url, endpoint, token, model)
    variables = {
            "now": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            }
    for name, expert in experts.items():
        response = await chat_gpt.post(expert, variables)
        print(f"{name}: {response}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
