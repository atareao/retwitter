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

import json
import logging

logger = logging.getLogger(__name__)


class Configuration:
    def __init__(self, config_file):
        logger.info("__init__")
        self._config_file = config_file

    def read(self):
        logger.info("read")
        with open(self._config_file, "r") as fr:
            self._config = json.load(fr)

    def save(self):
        logger.info("save")
        with open(self._config_file, "w") as fw:
            json.dump(self._config, fw, sort_keys=True, indent=4)

    def get(self, key, default=None):
        return self._config[key] if key in self._config else default

    def set(self, key, value):
        self._config[key] = value
