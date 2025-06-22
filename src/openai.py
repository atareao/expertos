#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from typing import List

from httpx import AsyncClient

logger = logging.getLogger(__name__)


class ChatGPT:
    """A class to manage ChatGPT."""

    def __init__(self, url: str, endpoint, token: str, model: str):
        """Initialize the ChatGPT class."""
        logger.info("__init__")
        self._url = f"https://{url}/{endpoint}"
        self._headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self._model = model

    async def post(self, messages: List[str]) -> str:
        """Send a message to ChatGPT and return the response."""
        logger.info("post")
        payload = {
            "model": self._model,
            "messages": messages
        }
        async with AsyncClient(timeout=None) as client:
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
    """Main function to run the program."""
    import tomllib
    from pprint import pprint

    import aiofiles
    from expertos.expert import Expert
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
    for name, expert in experts.items():
        response = await chat_gpt.post(expert)
        print(f"{name}: {response}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
