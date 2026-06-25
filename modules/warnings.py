import json
import os

FILE = "warnings.json"


def load():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_warn(user_id: int) -> int:
    data = load()
    return data.get(str(user_id), 0)


def add_warn(user_id: int) -> int:
    data = load()
    uid = str(user_id)
    data[uid] = data.get(uid, 0) + 1
    save(data)
    return data[uid]


def clear_warn(user_id: int):
    data = load()
    uid = str(user_id)
    if uid in data:
        del data[uid]
    save(data)
