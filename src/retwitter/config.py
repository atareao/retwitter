#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Configuraion module.

This module provides the Configuration class to manage configuration settings
from a JSON file.
"""

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
    """A class to manage the configuration settings.

    This class provides methods to read, save, get, and set configuration
    settings from a JSON file.
    """
    def __init__(self, config_file):
        """Initialize the Configuration with the given config file.

        :param config_file: Path to the configuration file.
        """
        logger.info("__init__")
        self._config = {}
        self._config_file = config_file

    def read(self):
        """Read the configuration from the file."""
        logger.info("read")
        with open(self._config_file, "r", encoding="utf-8") as fr:
            self._config = json.load(fr)

    def save(self):
        """Save the current configuration to the file."""
        logger.info("save")
        with open(self._config_file, "w", encoding="utf-8") as fw:
            json.dump(self._config, fw, sort_keys=True, indent=4)

    def get(self, key, default=None):
        """Get the value of the specified key from the configuration.

        :param key: The key to look up in the configuration.
        :param default: The default value to return if the key is not found.
        :return: The value associated with the key, or the default value.
        """
        return self._config[key] if key in self._config else default

    def set(self, key, value):
        """Set the value of the specified key in the configuration.

        :param key: The key to set in the configuration.
        :param value: The value to associate with the key.
        """
        self._config[key] = value
