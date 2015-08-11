#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Esther'
import splain_config
import tweepy
import traceback
import time
import random
import re
import simplejson as json

def login():
    # for info on the tweepy module, see http://tweepy.readthedocs.org/en/

    # Authentication is taken from splain_config.py
    consumer_key = splain_config.consumer_key
    consumer_secret = splain_config.consumer_secret
    access_token = splain_config.access_token
    access_token_secret = splain_config.access_token_secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api

def stick_together_output():
    occfile = open("occupations.json", "r", encoding="utf8")
    occfile = occfile.read()
    occs = json.loads(occfile)

    bases = set()

    for item in occs["occupations"]:
        if " " not in item.strip():
            bases.add(item)

    honfile = open("englishHonorifics.json", "r", encoding="utf8")
    honfile = honfile.read()
    hons = json.loads(honfile)

    for item in hons["englishHonorifics"]:
        if " " not in item.strip() and re.search("[AEIOUaeiou]", item):
            bases.add(item)

    output = (random.sample(bases, 1)[0]).lower()

    if output.endswith("s"):
        output += "plain"
    else:
        output += "splain"

    return output

def tweet_something(debug):
    api = login()
    try:
        output = stick_together_output()
        if debug:
            print(output)
        else:
            api.update_status(status=output)
            print(output)
    except:
        error_msg = traceback.format_exc().split("\n", 1)[1][-130:]
        api.send_direct_message(screen_name = "ojahnn", text = error_msg + " " + time.strftime("%H:%M:%S"))

tweet_something(False)