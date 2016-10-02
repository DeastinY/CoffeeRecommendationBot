#!/usr/bin/env python3.4
# Encoding: Utf-8
import random
from collections import OrderedDict, deque
# create a keys.py file with your twitter tokens if you want to run your own
# instance !
import keys
import logging
import json
from TwitterAPI import TwitterAPI, TwitterRequestError

logging.basicConfig(filename="/tmp/coffeebot.log", level=logging.INFO)

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
    """ () -> str

    Creates random order_dict of coffee with random multi,
    size, coffee, attribute, syrup_type, and syrup.
    """
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


def make_tweet(username):
    """ (str) -> str

    Given the twitter username of a twitter user, returns a tweet
    recommending user with a new coffee order.
    """
    while True:
        a, b = random.choice(intro)
        o = u"@{} {} {} {}".format(username, a, order(), b)
        if len(o) < 140:
            return o


logging.info("Connecting to Twitter API")
api = TwitterAPI(keys.consumer_key, keys.consumer_secret,
                 keys.access_token_key, keys.access_token_secret)
bot = api.request('account/verify_credentials').json()["screen_name"]
# we keep the last 1000 messages and do not reply to those again
msgs = deque(maxlen=1000)
logging.info("Connected")

try:
    for msg in api.request('user', {'replies': 'all'}):
        logging.info("New event")
        logging.debug(msg)
        if "text" in msg:
            logging.info("Event is Tweet")
            id = msg["id"]
            other = msg["user"]["screen_name"]
            to = msg["in_reply_to_screen_name"]
            toid = msg["in_reply_to_status_id"]
            logging.debug(other + " : " + msg["text"])
            if other == bot:
                logging.info("My own tweet")
                msgs.append(id)
            if to == bot and not other == bot and toid not in msgs:
                logging.info("Replying to tweet directed to me !")
                api.request('friendships/create', {'screen_name': other})
                t = make_tweet(other)
                r = api.request('statuses/update',
                                {'in_reply_to_status_id': id, 'status': t})
                logging.info("replied to {} with status {}"
                             .format(other, r.status_code))
                msgs.append(id)
            elif bot in msg["text"] and not other == bot:
                logging.info("Was mentioned ! Like or Retweet maybe ?")
                # friend them all !
                api.request('friendships/create', {'screen_name': other})
                if random.choice([True, False]):
                    api.request('favorites/create', {'id': id})
                if random.randint(0, 10) == 3:  # 1 in 10 chance for retweet
                    api.request('statuses/retweet/:id', {'id': id})
except TwitterRequestError as e:
    logging.exception(e)
