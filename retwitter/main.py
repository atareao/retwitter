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

import asyncio
import logging
import os
import sys
from time import time

from config import Configuration
from openobserve import OpenObserve
from retry import retry
from twitter import Twitter

FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
logging.basicConfig(stream=sys.stdout,
                    format=FORMAT,
                    level=logging.getLevelName(LOG_LEVEL))
logger = logging.getLogger(__name__)


@retry(tries=6, delay=600)
async def start_twitter(configuration: Configuration) -> Twitter:
    """Initialize and return a Twitter instance.

    Args:
        configuration (Configuration): The configuration object.

    Returns:
        Twitter: An initialized Twitter instance.
    """
    twitter = Twitter(configuration)
    await twitter.init()
    return twitter


async def main():
    """Main function to initialize configuration.

    Start the Twitter retweet process.
    """
    logger.info("main")
    config_file = os.getenv("CONFIG_FILE")
    configuration = Configuration(config_file)
    configuration.read()

    sleep_time = int(configuration.get("sleep_time", 600))

    openobserve = OpenObserve(configuration)
    twitter = await start_twitter(configuration)

    while True:
        try:
            tweet = await twitter.retweet_last()
            if tweet:
                message = {
                    "tweet_id": tweet.id,
                    "response": {
                        "id": tweet.id,
                        "created_at": tweet.created_at,
                        "user": tweet.user.name,
                        "text": tweet.text,
                        "lang": tweet.lang,
                        "quote_count": tweet.quote_count,
                        "reply_count": tweet.reply_count,
                        "favorite_count": tweet.favorite_count,
                        "view_count": tweet.view_count,
                        "retweet_count": tweet.retweet_count
                    }
                }
            else:
                message = {
                    "tweet_id": "",
                    "response": {
                        "id": "",
                        "created_at": time(),
                        "user": "",
                        "text": "No hay nuevos",
                        "lang": "es",
                        "quote_count": 0,
                        "reply_count": 0,
                        "favorite_count": 0,
                        "view_count": 0,
                        "retweet_count": 0
                    }
                }
            await openobserve.post(message)
        except Exception as exception:
            logger.error(exception)
        await asyncio.sleep(sleep_time)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(main())
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
