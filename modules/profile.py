import json
import os
from datetime import datetime


FILE = "users.json"


def load():

    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r") as f:
        return json.load(f)



def save(data):

    with open(FILE, "w") as f:
        json.dump(data, f)



def get_user(user):

    data = load()

    uid = str(user.id)


    if uid not in data:

        data[uid] = {
            "name": user.first_name,
            "coins": 0,
            "level": 1,
            "vip": False,
            "join": str(datetime.now())
        }

        save(data)


    return data[uid]



def add_coin(user, amount):

    data = load()

    uid = str(user.id)

    if uid not in data:
        get_user(user)
        data = load()


    data[uid]["coins"] += amount


    if data[uid]["coins"] >= 100:
        data[uid]["level"] += 1
        data[uid]["coins"] = 0


    save(data)
