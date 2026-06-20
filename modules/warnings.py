import json
import os

FILE = "warnings.json"


def load():
    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r") as f:
        return json.load(f)


def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f)


def add_warn(user_id):

    data = load()

    uid = str(user_id)

    if uid not in data:
        data[uid] = 0

    data[uid] += 1

    save(data)

    return data[uid]


def get_warn(user_id):

    data = load()

    return data.get(str(user_id), 0)


def clear_warn(user_id):

    data = load()

    uid = str(user_id)

    data[uid] = 0

    save(data)
