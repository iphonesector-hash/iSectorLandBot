import json
import os

FILE = "groups.json"


def load():
    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r") as f:
        return json.load(f)


def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f)


def register_group(chat):

    data = load()

    cid = str(chat.id)

    if cid not in data:

        data[cid] = {
            "title": chat.title,
            "warn_limit": 3,
            "auto_ban": False
        }

        save(data)


def get_group(chat_id):

    data = load()

    return data.get(str(chat_id))
