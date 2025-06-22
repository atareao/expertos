#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import re
from typing import Union

from httpx import AsyncClient

logger = logging.getLogger(__name__)


class Telegram:
    """Telegram API client."""
    def __init__(self, url: str, token: str):
        """Initialize the Telegram API client."""
        logger.info("__init__")
        self._url = f"https://{url}/bot{token}"
        self._headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    async def post(
        self, chat_id: Union[str, int], thread_id: int = 0, message: str = ""
    ):
        """Send a message to a Telegram chat."""
        logger.info("post")
        url = f"{self._url}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "message_thread_id": thread_id,
            "parse_mode": "HTML",
            "text": message.replace('"', "'"),
        }
        logger.debug(payload)
        print(payload)
        async with AsyncClient() as client:
            response = await client.post(
                url, headers=self._headers, json=payload
            )
            logger.debug(f"Response: {response}")
            if response.status_code == 200:
                return response.json()
            else:
                msg = f"HTTP Error: {response.status_code}"
                print(response)
                print(response.json())
                raise Exception(msg)

    async def postMarkdown(
        self, chat_id: Union[str, int], thread_id: int = 0, message: str = ""
    ):
        """Send a message to a Telegram chat using Markdown formatting."""
        logger.info("post")
        url = f"{self._url}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "message_thread_id": thread_id,
            "parse_mode": "MarkdownV2",
            "text": self.escape_markdown_v2(message)
        }
        logger.debug(payload)
        print(payload)
        async with AsyncClient() as client:
            response = await client.post(
                url, headers=self._headers, json=payload
            )
            logger.debug(f"Response: {response}")
            if response.status_code == 200:
                return response.json()
            else:
                msg = f"HTTP Error: {response.status_code}"
                print(response)
                print(response.json())
                raise Exception(msg)

    def escape_markdown_v2(self, text: str) -> str:
        """Escapes all special characters in a MarkdownV2 text."""
        text = text.replace('"', "'")
        escape_chars = r"~#+-={}[]().\\"
        def escape_char(match):
            return '\\' + match.group(0)
        text = re.sub(f'([{re.escape(escape_chars)}])', escape_char, text)
        return text
