#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2024 Lorenzo Carbonell <a.k.a. atareao>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sqlite3

from log import Log


class DB:
    """Database class for managing SQLite databases."""
    @Log.info
    def __init__(self, filename: str):
        """Initialize the database connection."""
        self._filename = filename

    @Log.info
    def execute(self, script: str):
        """Execute a SQL script."""
        with sqlite3.connect(self._filename) as connection:
            cursor = connection.cursor()
            cursor.execute(script)

    @Log.info
    def select(self, sql: str, values=None):
        """Execute a SQL SELECT statement and return the results."""
        with sqlite3.connect(self._filename) as connection:
            cursor = connection.cursor()
            if values:
                res = cursor.execute(sql, values)
            else:
                res = cursor.execute(sql)
            return res.fetchall()

    @Log.info
    def insert(self, sql: str, values):
        """Insert data into a table."""
        with sqlite3.connect(self._filename) as connection:
            cursor = connection.cursor()
            res = cursor.execute(sql, values)
            connection.commit()
            if sql.find(" RETURNING ") > -1:
                return res.fetchall()

    @Log.info
    def update(self, sql: str, values):
        """Update data in a table."""
        with sqlite3.connect(self._filename) as connection:
            cursor = connection.cursor()
            res = cursor.execute(sql, values)
            connection.commit()
            if sql.find(" RETURNING ") > -1:
                return res.fetchall()

    @Log.info
    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists."""
        sql = ("SELECT name FROM sqlite_master WHERE type='table' AND "
               "name = ? ")
        values = self.select(sql, (table_name,))
        if values:
            return values[0][0] == table_name
        return False
