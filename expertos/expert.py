#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from typing import List, Dict
from jinja2 import Template

logger = logging.getLogger(__name__)


class Expert:
    def __init__(self, data: Dict[str, str]):
        self._name = data["name"]
        self._prompt = data["prompt"]
        self._question = data["question"]
        self._chat_id = data["chat_id"]
        self._thread_id = data["thread_id"]

    def get_chat_id(self):
        return self._chat_id

    def get_thread_id(self):
        return self._thread_id

    def messages(self, variables) -> List[Dict[str, str]]:
        template_prompt = Template(self._prompt)
        prompt = template_prompt.render(variables)
        template_question = Template(self._question)
        question = template_question.render(variables)
        logger.debug(f"prompt: {prompt}")
        logger.debug(f"question: {question}")
        return [
                {"role": "system", "content": prompt},
                {"role": "user", "content": question},
            ]
