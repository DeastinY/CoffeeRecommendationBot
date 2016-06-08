# Encoding: Utf-8
import os
import time
import random
import keys  # create a keys.py file with your twitter tokens if you want to run your own instance !
import twitter
from collections import OrderedDict

intro = [("How about a","?"), ("Why not try the","?"), ("Try a","!"), ("Check out a","!"), ("Nothing like a",".")]
multi = ["","Single", "Double", "Tripple", "Quad"]
size = ["Short", "Tall", "Grande", "Venti® Hot", "Venti® Cold", "Trenta® Cold"]
coffee = ["Espresso", "Espresso Macchiato", "Espresso con Panna", "Caffe Americano", "Cappuccino", "Caffe Latte", "Vanilla Latte", "Caramel Macchiato", "Chocolate Mocha", "White Caffe Mocha", "Frappuccino", "Ristretto", "Chai Tea Latte"]
attribute = ["","Non-Fat", "Iced", "Sugar Free", "Venti", "Soy", "No Foam", "Triple", "Half Sweet", "Decaf", "Half-Caff" , "Quad", "One-Pump", "Skinny", "Sugar-Free Syrup", "Light Ice", "No Whip", "Dolce Soy"]
syrup_type = ["","Extra Hot", "Non-Fat", "Half-Sweet", "One-Pump", "Ten-Pump", "4-Pump"]
syrup = ["", "Caramel", "Hazelnut", "Cinnamon"]
appendition = ["" ,"Extra Shot", "Extra Whip", "With An Extra Shot And Cream", "At 120 Degrees", "With Extra Whipped Cream and Chocolate Sauce"]

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

def make_tweet(username):
    while True:
        a, b = random.choice(intro)
        o = u"@"+username+" "+a+" "+order()+" "+b
        if len(o) < 140:
            return o

def load_ids():
    with open("ids.txt","r") as f:
        return f.read().split(";")
    return None

def save_ids(ids):
    with open("ids.txt","w") as f:
        f.write(";".join(ids))

api = twitter.Api(consumer_key=keys.consumer_key, consumer_secret=keys.consumer_secret, access_token_key=keys.access_token_key, access_token_secret=keys.access_token_secret)

ids = load_ids() or []

#tweets = api.GetSearch(term="Coffee", count=200)
mentions = api.GetMentions(count=200)
timeline = api.GetHomeTimeline(count=200)

followers = api.GetFollowerIDs()
# follow back
for f in followers:
    api.CreateFriendship(f,follow=True)


for t in timeline + mentions:
    if not t.id in ids and t.user.id in followers: # only hit up followers
        tweet = make_tweet(t.user.screen_name)
        ret = api.PostUpdate(tweet,in_reply_to_status_id=t.id)
        ids.append(t.id_str)
        print(ret)
        break
save_ids(ids)

