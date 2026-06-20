import json
import os


FILE = "group_settings.json"


default = {
    "spam": True,
    "link": True,
    "mention": True
}


def load():

    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r") as f:
        return json.load(f)



def save(data):

    with open(FILE, "w") as f:
        json.dump(data, f)



def get(chat_id):

    data = load()

    if str(chat_id) not in data:
        data[str(chat_id)] = default.copy()
        save(data)

    return data[str(chat_id)]



def set_option(chat_id, key, value):

    data = load()

    if str(chat_id) not in data:
        data[str(chat_id)] = default.copy()


    data[str(chat_id)][key] = value

    save(data)
