#!/usr/bin/env python3.4
# Encoding: Utf-8
import random
from collections import deque
# create a keys.py file with your twitter tokens if you want to run your own
# instance !
import keys
import logging
import json
from TwitterAPI import TwitterAPI, TwitterRequestError

try:
    xrange
except NameError:
    xrange = range

logging.basicConfig(filename='/tmp/coffeebot.log', level=logging.INFO)

coffee_file = open('coffeeType.json')
coffee_types = json.load(coffee_file)


def order():
    """ () -> str

    Creates random order of coffee with random multi,
    size, coffee, attribute, syrup_type, and syrup.
    """
    current_order = [random.choice(coffee_types['multi'])]

    for _ in xrange(random.randint(0, 5)):
        current_order.append(random.choice(coffee_types['attribute']))

    current_order.extend([random.choice(coffee_types['size']),
                          random.choice(list(coffee_types['coffee'].keys())),
                          random.choice(coffee_types['syrup_type']),
                          random.choice(coffee_types['syrup'])])

    for _ in xrange(random.randint(0, 2)):
        current_order.append(random.choice(coffee_types['appendition']))
    print(current_order)
    return ' '.join(current_order)


def make_tweet(username=False):
    """ (str) -> str

    Given the twitter username of a twitter user, returns a tweet
    recommending user with a new coffee order.
    """
    if username:
        while True:
            a = random.choice(coffee_types['intro'])
            o = u'@{} {} {} '.format(username, a, order())
            if len(o) < 140:
                return o
    else:
        while True:
            o = u'Coffee of the day :\n' + order()
            if len(o) < 140:
                return o


def daily_coffee():
    logging.info('Sending COTD')
    t = make_tweet()
    r = api.request('statuses/update', {'status': t})
    logging.info('COTD with status : {}'.format(r.status_code))
    logging.info('Done !')


logging.info('Connecting to Twitter API')
api = TwitterAPI(keys.consumer_key, keys.consumer_secret,
                 keys.access_token_key, keys.access_token_secret)
bot = api.request('account/verify_credentials').json()['screen_name']
# we keep the last 1000 messages and do not reply to those again
msgs = deque(maxlen=1000)
logging.info('Connected')

try:
    daily_coffee()
except TwitterRequestError as e:
    logging.exception(e)

try:
    for msg in api.request('user', {'replies': 'all'}):
        logging.info('New event')
        logging.debug(msg)
        if 'text' in msg:
            logging.info('Event is Tweet')
            msg_id = msg['id']
            other = msg['user']['screen_name']
            to = msg['in_reply_to_screen_name']
            toid = msg['in_reply_to_status_id']
            logging.debug(other + ' : ' + msg['text'])
            if other == bot:
                logging.info('My own tweet')
                msgs.append(msg_id)
            if to == bot and not other == bot and toid not in msgs:
                logging.info('Replying to tweet directed to me !')
                api.request('friendships/create', {'screen_name': other})
                tweet = make_tweet(other)
                response = api.request('statuses/update',
                                       {'in_reply_to_status_id': msg_id,
                                        'status': tweet})
                logging.info('replied to {} with status {}'
                             .format(other, response.status_code))
                msgs.append(msg_id)
            elif bot in msg['text'] and not other == bot:
                logging.info('Was mentioned ! Like or Retweet maybe ?')
                # friend them all !
                api.request('friendships/create', {'screen_name': other})
                if random.choice([True, False]):
                    api.request('favorites/create', {'id': msg_id})
                if random.randint(0, 10) == 3:  # 1 in 10 chance for retweet
                    api.request('statuses/retweet/:id', {'id': msg_id})
except TwitterRequestError as e:
    logging.exception(e)
