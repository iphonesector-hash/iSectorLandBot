import json
import os


FILE = "locks.json"


def load():

    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)



def save(data):

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )



def get_chat(chat_id):

    data = load()

    cid = str(chat_id)

    if cid not in data:

        data[cid] = {
            "bad_words": False,
            "words": False,
            "links": False,
            "list": []
        }

        save(data)

    return data[cid]



async def lock_bad(update, context):

    data = get_chat(
        update.effective_chat.id
    )

    data["bad_words"] = True

    save(load())


    await update.message.reply_text(
        "🔒 قفل فحش فعال شد"
    )



async def unlock_bad(update, context):

    data = get_chat(
        update.effective_chat.id
    )

    data["bad_words"] = False

    save(load())


    await update.message.reply_text(
        "🔓 قفل فحش خاموش شد"
    )



async def lock_words(update, context):

    data = get_chat(
        update.effective_chat.id
    )

    data["words"] = True

    save(load())


    await update.message.reply_text(
        "🔒 قفل کلمات فعال شد"
    )



async def unlock_words(update, context):

    data = get_chat(
        update.effective_chat.id
    )

    data["words"] = False

    save(load())


    await update.message.reply_text(
        "🔓 قفل کلمات خاموش شد"
    )



async def lock_links(update, context):

    data = get_chat(
        update.effective_chat.id
    )

    data["links"] = True

    save(load())


    await update.message.reply_text(
        "🔒 قفل لینک فعال شد"
    )



async def unlock_links(update, context):

    data = get_chat(
        update.effective_chat.id
    )

    data["links"] = False

    save(load())


    await update.message.reply_text(
        "🔓 قفل لینک خاموش شد"
    )



async def check_locks(update, context):

    if not update.message:
        return


    text = update.message.text

    chat = update.effective_chat

    cfg = get_chat(chat.id)



    bad_words = [
        "فحش",
        "بد"
    ]



    if cfg["bad_words"]:

        for word in bad_words:

            if word in text:

                await update.message.delete()

                await update.message.reply_text(
                    "⚠️ پیام حذف شد (فیلتر فحش)"
                )

                return



    if cfg["links"]:

        if "http://" in text or "https://" in text:

            await update.message.delete()

            await update.message.reply_text(
                "🔗 ارسال لینک ممنوع است"
            )

            return



    if cfg["words"]:

        for word in cfg["list"]:

            if word in text:

                await update.message.delete()

                await update.message.reply_text(
                    "🚫 کلمه غیرمجاز استفاده شد"
                )

                return
