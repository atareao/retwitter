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

from config import Configuration
from twikit import Client

logger = logging.getLogger(__name__)


class Twitter:
    """A class to interact with Twitter using the provided configuration.

    This class handles authentication, fetching user tweets, and retweeting
    the latest tweets.
    """
    def __init__(self, configuration: Configuration):
        """Initialize the Twitter client with the given configuration.

        :param configuration: Configuration object containing user credentials
        and settings.
        """
        logger.info("__init__")
        self._configuration = configuration
        self._is_auth = False
        self._client = Client("es-ES")
        self._user = None

    async def init(self):
        """Asynchronously initialize the Twitter client.

        This method logs in the client using the credentials provided in the
        configuration and retrieves the user information based on the user ID.
        """
        await self._client.login(
            auth_info_1=self._configuration.get("username"),
            auth_info_2=self._configuration.get("mail"),
            password=self._configuration.get("password")
        )
        self._is_auth = True
        user_id = self._configuration.get("user_id")
        self._user = await self._client.get_user_by_id(user_id)

    async def retweet_last(self):
        """Asynchronously retweet the latest tweet that is not a retweet.

        This method fetches the latest tweets, filters out retweets, and
        retweets the most recent tweet.  It also updates the configuration with
        the ID of the last retweeted tweet.
        """
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
        """Destructor method to log out the client if authenticated.

        This method ensures that the client logs out when the Twitter object is
        destroyed, provided that the client was authenticated.
        """
        logger.info("__del__")
        if self._is_auth:
            response = self._client.logout()
            logger.debug(response)


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    one_configuration = Configuration("config.json")
    one_configuration.read()
    t = Twitter(one_configuration)
    tasks = [
        loop.create_task(t.retweet_last())
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
