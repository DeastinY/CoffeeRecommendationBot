#!/usr/bin/env python3.4
# Encoding: Utf-8
import random
from collections import OrderedDict
# create a keys.py file with your twitter tokens
# if you want to run your own instance !
import keys
import logging
import json
from TwitterAPI import TwitterAPI, TwitterRequestError

coffee_file = open("coffeeType.json")
coffee_types = json.load(coffee_file)
intro = coffee_types['intro']
multi = coffee_types['multi']
size = coffee_types['size']
coffee = coffee_types['coffee']
attribute = coffee_types['attribute']
syrup_type = coffee_types['syrup_type']
syrup = coffee_types['syrup']
appendition = coffee_types['appendition']


def order():
    order_dict = OrderedDict()
    order_dict[random.choice(multi)] = True
    for i in range(random.randint(0, 5)):
        order_dict[random.choice(attribute)] = True
    order_dict[random.choice(size)] = True
    order_dict[random.choice(coffee)] = True
    order_dict[random.choice(syrup_type)] = True
    order_dict[random.choice(syrup)] = True
    for i in range(random.randint(0, 2)):
        order_dict[random.choice(appendition)] = True
    return " ".join(" ".join(order_dict.keys()).split())


def make_tweet():
    while True:
        o = u"Coffee of the day :\n" + order()
        if len(o) < 140:
            return o


logging.info("Connecting to Twitter API")
api = TwitterAPI(
    keys.consumer_key,
    keys.consumer_secret,
    keys.access_token_key,
    keys.access_token_secret
)
bot = api.request('account/verify_credentials').json()["screen_name"]
logging.info("Connected")

try:
    logging.info("Sending COTD")
    t = make_tweet()
    r = api.request('statuses/update', {'status': t})
    logging.info("COTD with status : {}".format(r.status_code))
    logging.info("Done !")
except TwitterRequestError as e:
    logging.exception(e)
