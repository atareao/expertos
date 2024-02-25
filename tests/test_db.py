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

import os
from expertos.db import DB
from expertos import log

FILENAME = "test.db"
TABLENAME = "test"


class TestDB:
    def setup_class(self):
        if os.path.exists(FILENAME):
            os.remove(FILENAME)
        sql = (f"CREATE TABLE IF NOT EXISTS {TABLENAME} ("
               "id INTEGER PRIMERY KEY,"
               "message TEXT NOT NULL DEFAULT '');")
        self.db = DB(FILENAME)
        self.db.execute(sql)

    def teardown_class(self):
        if os.path.exists(FILENAME):
            os.remove(FILENAME)

    @log.info
    def test_db_exists(self):
        sql = ("SELECT name FROM sqlite_master WHERE type='table' AND "
               "name = ? ")
        values = self.db.select(sql, (TABLENAME,))
        log.debug(values)
        assert values is not None
        assert values[0][0] == TABLENAME
