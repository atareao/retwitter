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
import requests
from requests_oauthlib import OAuth1


logger = logging.getLogger(__name__)


class Twitter:
    def __init__(self, consumer_key: str, consumer_secret: str,
                 access_token: str, access_secret: str):
        logger.info("__init__")
        self._oauth = OAuth1(consumer_key, client_secret=consumer_secret,
                             resource_owner_key=access_token,
                             resource_owner_secret=access_secret)

    def retweet(self, tweet_id):
        logger.info("retweet")
        url = f"https://api.twitter.com/1.1/statuses/retweet/{tweet_id}.json"
        logger.info(f"Url to retweet {url}")
        response = requests.post(url=url, auth=self._oauth)
        if response.status_code == 200:
            logger.info(f"Retweeted: {tweet_id}")
            return response.json()
        msg = (f"Can not retweet: {tweet_id}. "
               f"HTTP Error: {response.status_code}. {response.text}")
        raise Exception(msg)

    def get_last_tweet(self, user_id, last_id) -> int:
        logger.info("get_last_tweet")
        if last_id:
            url = ("https://api.twitter.com/1.1/statuses/user_timeline.json?"
                   f"user_id={user_id}&since_id={last_id}")
        else:
            url = ("https://api.twitter.com/1.1/statuses/user_timeline.json?"
                   f"user_id={user_id}")

        response = requests.get(url=url)
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]['id']
            else:
                msg = "Can not get last tweet"
                raise Exception(msg)
        else:
            msg = f"HTTP Error: {response.status_code}. {response.text}"
            raise Exception(msg)
