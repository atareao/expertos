#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from httpx import AsyncClient
from expert import Expert

logger = logging.getLogger(__name__)


class Telegram:
    def __init__(self, url: str, token: str):
        logger.info("__init__")
        self._url = f"https://{url}/bot{token}"
        self._headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    async def post(self, expert: Expert, message: str):
        logger.info("post")
        url = f"{self._url}/sendMessage"
        payload = {
                "chat_id": int(expert.get_chat_id()),
                "message_thread_id": int(expert.get_thread_id()),
                "parse_mode": "markdown",
                "text": message
                }
        logger.debug(payload)
        print(payload)
        async with AsyncClient() as client:
            response = await client.post(
                    url, headers=self._headers, json=payload)
            logger.debug(f"Response: {response}")
            if response.status_code == 200:
                return response.json()
            else:
                msg = f"HTTP Error: {response.status_code}"
                print(response)
                print(response.json())
                raise Exception(msg)
