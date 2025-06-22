#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from typing import Dict, List

from jinja2 import Template

from db import DB

logger = logging.getLogger(__name__)


class Expert:
    """Expert class for generating dialogues."""
    def __init__(self, db: DB, data: Dict[str, str]):
        """Initialize an Expert object."""
        self._name = data["name"]
        self._prompt = data["prompt"]
        self._question = data["question"]
        self._db = db

    def get_dialog(self) -> List[Dict[str, str]]:
        """Generate a dialogue for the expert."""
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
        """Get variables for the expert."""
        variables = {"now": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
        return variables
