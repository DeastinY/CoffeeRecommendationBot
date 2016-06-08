# Encoding: Utf-8
import random
import keys  # create a keys.py file with your twitter tokens if you want to run your own instance !
import twitter
from collections import OrderedDict

intro = [("How about a","?"), ("Why not try the","?"), ("Try a","!"), ("Check out a","!"), ("Nothing like a",".")]
multi = ["","Single", "Double", "Tripple", "Quad"]
size = ["Short", "Tall", "Grande", "Venti® Hot", "Venti® Cold", "Trenta® Cold"]
coffee = ["Espresso", "Espresso Macchiato", "Espresso con Panna", "Caffe Americano", "Cappuccino", "Caffe Latte", "Vanilla Latte", "Caramel Macchiato", "Chocolate Mocha", "White Caffe Mocha", "Frappuccino", "Ristretto", "Chai Tea Latte"]
type = ["","Non-Fat", "Iced", "Sugar Free", "Venti", "Soy", "No Foam", "Triple", "Half Sweet", "Decaf", "Half-Caff" , "Quad", "One-Pump", "Skinny", "Sugar-Free Syrup", "Light Ice", "No Whip", "Dolce Soy"]
syrup_type = ["","Extra Hot", "Non-Fat", "Half-Sweet", "One-Pump", "Ten-Pump", "4-Pump"]
syrup = ["", "Caramel", "Hazelnut", "Cinnamon"]
appendition = ["" ,"Extra Shot", "Extra Whip", "With An Extra Shot And Cream", "At 120 Degrees", "With Extra Whipped Cream and Chocolate Sauce"]

def order():
    order = OrderedDict()
    order[random.choice(multi)] = True
    for i in range(5):
        order[random.choice(type)] = True
    order[random.choice(size)] = True
    order[random.choice(coffee)] = True
    order[random.choice(syrup_type)] = True
    order[random.choice(syrup)] = True
    for i in range(2):
        order[random.choice(appendition)] = True
    return " ".join(" ".join(order.keys()).split())

def make_tweet():
    while True:
        a, b = random.choice(intro)
        o = a+" "+order()+" "+b
        if len(o) < 140:
            return o

api = twitter.Api(consumer_key=keys.consumer_key, consumer_secret=keys.consumer_secret, access_token_key=keys.access_token_key, access_token_secret=keys.access_token_secret)
status = api.PostUpdate(make_tweet())
