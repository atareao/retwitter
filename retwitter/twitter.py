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


import logging
from twikit import Client
from config import Configuration

logger = logging.getLogger(__name__)


class Twitter:
    def __init__(self, configuration: Configuration):
        logger.info("__init__")
        self._configuration = configuration
        self._is_auth = False
        self._client = Client("es-ES")

    async def init(self):
        await self._client.login(
            auth_info_1=self._configuration.get("username"),
            auth_info_2=self._configuration.get("mail"),
            password=self._configuration.get("password")
        )
        self._is_auth = True
        user_id = self._configuration.get("user_id")
        self._user = await self._client.get_user_by_id(user_id)

    async def retweet_last(self):
        logger.info("retweet_last")
        last_id = int(self._configuration.get("last_id", 0))
        tweets = list(await self._user.get_tweets("Tweets", 10))
        tweets.sort(key=lambda x: x.id)
        last_tweets = list(filter(
            lambda x: int(x.id) > last_id and not x.text.startswith("RT "),
            tweets))
        if last_tweets:
            last_tweet = last_tweets[0]
            await last_tweet.retweet()
            self._configuration.set("last_id", int(last_tweet.id))
            self._configuration.save()
            return last_tweet
        return None

    def __del__(self):
        logger.info("__del__")
        if self._is_auth:
            response = self._client.logout()
            logger.debug(response)


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    configuration = Configuration("config.json")
    configuration.read()
    t = Twitter(configuration)
    tasks = [
        loop.create_task(t.retweet_last())
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
