#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Class to interact with the OpenObserve API.
This module provides the OpenObserve class for interacting with the OpenObserve
API.
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

from logging import getLogger
from typing import Dict

import aiohttp

from retwitter.config import Configuration

logger = getLogger(__name__)


class OpenObserve:
    """OpenObserve class handles the interaction with the OpenObserve API."""

    def __init__(self, configuration: Configuration) -> None:
        """Initialize the OpenObserve instance with the given configuration.

        :param configuration: Configuration object containing OpenObserve
               settings.
        """
        logger.info("__init__")
        self._token = configuration.get("openobserve_token", "")
        self._base_url = configuration.get("openobserve_base_url", "")
        self._index = configuration.get("openobserve_index", "")

    async def post(self, message: Dict):
        """Post a message to the OpenObserve API.

        :param message: Dictionary containing the message to be posted.
        """
        logger.info("__post__")
        if self._token == "" or self._base_url == "" or self._index == "":
            return
        logger.debug("message: %s", message)
        url = f"https://{self._base_url}/api/default/{self._index}/_json"
        headers = {"Authorization": f"Basic {self._token}",
                   "Content-Type": "application/json",
                   "Accept": "application/json"}
        try:
            data = [message]
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers,
                                        json=data) as response:
                    content = await response.text()
                    logger.debug("response: %s. %s", response.status, content)
                    if response.status != 200:
                        msg = f"HTTP Error {response.status}. {content}"
                        raise Exception(msg)
        except Exception as exception:
            logger.error(exception)
