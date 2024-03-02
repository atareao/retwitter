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
import os
from openobserve import OpenObserve
from retwitter.config import Configuration
from time import sleep
from twitter import Twitter

logger = logging.getLogger(__name__)


def main():
    logger.info("main")
    config_file = os.getenv("CONFIG_FILE")
    configuration = Configuration(config_file)
    configuration.read()

    sleep_time = configuration.config["sleep_time"]
    user_id = configuration.config["user_id"]
    last_id = configuration.config["last_id"]

    openobserve_token = configuration.config["openobserve_token"]
    openobserve_base_url = configuration.config["openobserve_base_url"]
    openobserve_index = configuration.config["openobserve_index"]
    openobserve = OpenObserve(openobserve_base_url, openobserve_token,
                              openobserve_index)

    consumer_key = configuration.config["consumer_key"]
    consumer_secret = configuration.config["consumer_secret"]
    access_token = configuration.config["access_token"]
    access_secret = configuration.config["access_secret"]
    twitter = Twitter(consumer_key, consumer_secret, access_token,
                      access_secret)

    while True:
        try:
            last_id = twitter.get_last_tweet(user_id, last_id)
            response = twitter.retweet(last_id)
            configuration.config["last_id"] = last_id
            configuration.save()
            message = {
                "tweet_id": last_id,
                "response": response
            }
            openobserve.post(message)
        except Exception as exception:
            logger.error(exception)
        sleep(sleep_time)


if __name__ == "__main__":
    main()
