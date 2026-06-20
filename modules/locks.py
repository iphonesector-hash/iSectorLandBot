import json
import os


FILE = "locks.json"


def load():

    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r") as f:
        return json.load(f)



def save(data):

    with open(FILE, "w") as f:
        json.dump(data, f)



def get_chat(chat_id):

    data = load()

    cid = str(chat_id)

    if cid not in data:

        data[cid] = {
            "bad_words": False,
            "words": False,
            "links": False
        }

        save(data)

    return data[cid]



async def lock_bad(update, context):

    chat = update.effective_chat

    data = get_chat(chat.id)

    data["bad_words"] = True

    save(load())

    await update.message.reply_text(
        "🔒 قفل فحش فعال شد"
    )



async def unlock_bad(update, context):

    chat = update.effective_chat

    data = get_chat(chat.id)

    data["bad_words"] = False

    save(load())

    await update.message.reply_text(
        "🔓 قفل فحش خاموش شد"
    )



async def lock_words(update, context):

    chat = update.effective_chat

    data = get_chat(chat.id)

    data["words"] = True

    save(load())

    await update.message.reply_text(
        "🔒 قفل کلمات فعال شد"
    )



async def unlock_words(update, context):

    chat = update.effective_chat

    data = get_chat(chat.id)

    data["words"] = False

    save(load())

    await update.message.reply_text(
        "🔓 قفل کلمات خاموش شد"
    )



async def check_locks(update, context):

    if not update.message:
        return


    text = update.message.text

    chat = update.effective_chat

    cfg = get_chat(chat.id)


    bad = [
        "فحش1",
        "فحش2"
    ]


    if cfg["bad_words"]:

        for w in bad:

            if w in text:

                await update.message.delete()

                await update.message.reply_text(
                    "⚠️ پیام به دلیل فحش حذف شد"
                )

                return
