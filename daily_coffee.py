#!/usr/bin/env python3.4
# Encoding: Utf-8
import random
from collections import OrderedDict, deque
import keys  # create a keys.py file with your twitter tokens if you want to run your own instance !
import logging
from TwitterAPI import TwitterAPI, TwitterRequestError

intro = [("How about a","?"), ("Why not try the","?"), ("Try a","!"), ("Check out a","!"), ("Nothing like a",".")]
multi = ["","Single", "Double", "Tripple", "Quad"]
size = ["Short", "Tall", "Grande", "Venti® Hot", "Venti® Cold", "Trenta® Cold"]
coffee = ["Espresso", "Espresso Macchiato", "Espresso con Panna", "Caffe Americano", "Cappuccino", "Caffe Latte", "Vanilla Latte", "Caramel Macchiato", "Chocolate Mocha", "White Caffe Mocha", "Frappuccino", "Ristretto", "Chai Tea Latte"]
attribute = ["","Non-Fat", "Iced", "Sugar Free", "Venti", "Soy", "No Foam", "Tripple", "Half Sweet", "Decaf", "Half-Caff" , "Quad", "One-Pump", "Skinny", "Sugar-Free Syrup", "Light Ice", "No Whip", "Dolce Soy"]
syrup_type = ["","With Extra Hot", " And Non-Fat", " On Half-Sweet", " Add One-Pump", "Add Ten-Pump", "And 4-Pump"]
syrup = ["", "Caramel", "Hazelnut", "Cinnamon"]
appendition = ["" ,"And Extra Shot", " Plus Extra Whip", "With An Extra Shot And Cream", "At 120 Degrees", "With Extra Whipped Cream and Chocolate Sauce"]

def order():
    order = OrderedDict()
    order[random.choice(multi)] = True
    for i in range(random.randint(0,5)):
        order[random.choice(attribute)] = True
    order[random.choice(size)] = True
    order[random.choice(coffee)] = True
    order[random.choice(syrup_type)] = True
    order[random.choice(syrup)] = True
    for i in range(random.randint(0,2)):
        order[random.choice(appendition)] = True
    return " ".join(" ".join(order.keys()).split())

def make_tweet():
    while True:
        o = u"Coffee of the day :\n"+order()
        if len(o) < 140:
            return o

logging.info("Connecting to Twitter API")
api = TwitterAPI(keys.consumer_key, keys.consumer_secret, keys.access_token_key, keys.access_token_secret)
bot = api.request('account/verify_credentials').json()["screen_name"]
logging.info("Connected")

try:
    logging.info("Sending COTD")
    t = make_tweet()
    r = api.request('statuses/update', {'status' : t})
    logging.info("COTD with status : {}".format(r.status_code))
    logging.info("Done !")
except TwitterRequestError as e:
    logging.exception(e)
