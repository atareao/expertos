#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
from typing import Dict

from db import DB
from expert import Expert
from log import Log


class PythonExpert(Expert):
    """Python expert class."""
    def __init__(self, db: DB, data: Dict[str, str]):
        """Initialize the Python expert class."""
        super().__init__(db, data)
        self._table_name = "python_expert"
        if not self._db.table_exists(self._table_name):
            Log.debug(f"Table {self._table_name} not exists")
            self.configure_db()

    def configure_db(self):
        """Configure the database for the Python expert class."""
        sql = (f"CREATE TABLE IF NOT EXISTS {self._table_name} ("
               "id INTEGER PRIMARY KEY,"
               "module TEXT NOT NULL DEFAULT '',"
               "published BOOLEAN NOT NULL DEFAULT FALSE)")
        self._db.execute(sql)
        sql = f"INSERT INTO {self._table_name} (module) VALUES (?)"
        for module in self.modules():
            self._db.insert(sql, (module,))

    @staticmethod
    def modules():
        """Return an iterator of Python modules."""
        modules_file = os.path.join(os.path.dirname(__file__), "data",
                                    "python_modules.txt")
        with open(modules_file, "r") as fr:
            modules = fr.readlines()
        return iter(modules)

    def get_variables(self):
        """Return a dictionary of variables for the Python expert class."""
        variables = super().get_variables()
        sql = f"SELECT * FROM {self._table_name} WHERE published = ?"
        values = self._db.select(sql, (False,))
        selected = random.choice(values)
        Log.debug(selected)
        variables.update({"module": selected[1]})
        sql = f"UPDATE {self._table_name} SET published = ? WHERE id = ?"
        values = self._db.update(sql, (True, selected[0]))
        Log.debug(values)
        return variables
