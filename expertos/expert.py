#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from typing import List, Dict
from jinja2 import Template
from datetime import datetime

logger = logging.getLogger(__name__)


class Expert:
    def __init__(self, data: Dict[str, str]):
        self._name = data["name"]
        self._prompt = data["prompt"]
        self._question = data["question"]

    def messages(self) -> List[Dict[str, str]]:
        template_prompt = Template(self._prompt)
        variables = self.get_variables()
        prompt = template_prompt.render(variables)
        template_question = Template(self._question)
        question = template_question.render(variables)
        logger.debug(f"prompt: {prompt}")
        logger.debug(f"question: {question}")
        return [
                {"role": "system", "content": prompt},
                {"role": "user", "content": question},
            ]

    def get_variables(self):
        variables = {"now": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
        return variables
