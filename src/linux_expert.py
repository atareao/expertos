#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
from typing import Dict
from log import Log
from db import DB
from expert import Expert


class LinuxExpert(Expert):
    def __init__(self, db: DB, data: Dict[str, str]):
        super().__init__(db, data)
        self._table_name = "linux_expert"
        if not self._db.table_exists(self._table_name):
            Log.debug(f"Table {self._table_name} not exists")
            self.configure_db()

    def configure_db(self):
        sql = (f"CREATE TABLE IF NOT EXISTS {self._table_name} ("
               "id INTEGER PRIMARY KEY,"
               "command TEXT NOT NULL DEFAULT '',"
               "published BOOLEAN NOT NULL DEFAULT FALSE)")
        self._db.execute(sql)
        sql = f"INSERT INTO {self._table_name} (command) VALUES (?)"
        for command in self.commands():
            self._db.insert(sql, (command,))

    @staticmethod
    def commands():
        commands_file = os.path.join(os.path.dirname(__file__),
                                     "data",
                                     "linux_commands.txt")
        with open(commands_file, "r") as fr:
            commands = fr.readlines()
        return iter(commands)

    def get_variables(self):
        variables = super().get_variables()
        sql = f"SELECT * FROM {self._table_name} WHERE published = ?"
        values = self._db.select(sql, (False,))
        selected = random.choice(values)
        Log.debug(selected)
        variables.update({"command": selected[1]})
        sql = f"UPDATE {self._table_name} SET published = ? WHERE id = ?"
        values = self._db.update(sql, (True, selected[0]))
        Log.debug(values)
        return variables
