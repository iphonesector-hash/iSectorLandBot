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



# قفل فحش

async def lock_bad(update, context):

    cfg = get_chat(update.effective_chat.id)

    cfg["bad_words"] = True

    data = load()
    data[str(update.effective_chat.id)] = cfg
    save(data)


    await update.message.reply_text(
        "🔒 قفل فحش فعال شد"
    )



async def unlock_bad(update, context):

    cfg = get_chat(update.effective_chat.id)

    cfg["bad_words"] = False

    data = load()
    data[str(update.effective_chat.id)] = cfg
    save(data)


    await update.message.reply_text(
        "🔓 قفل فحش خاموش شد"
    )



# قفل کلمات

async def lock_words(update, context):

    cfg = get_chat(update.effective_chat.id)

    cfg["words"] = True

    data = load()
    data[str(update.effective_chat.id)] = cfg
    save(data)


    await update.message.reply_text(
        "🔒 قفل کلمات فعال شد"
    )



async def unlock_words(update, context):

    cfg = get_chat(update.effective_chat.id)

    cfg["words"] = False

    data = load()
    data[str(update.effective_chat.id)] = cfg
    save(data)


    await update.message.reply_text(
        "🔓 قفل کلمات خاموش شد"
    )



# لینک

async def lock_links(update, context):

    cfg = get_chat(update.effective_chat.id)

    cfg["links"] = True

    data = load()
    data[str(update.effective_chat.id)] = cfg
    save(data)


    await update.message.reply_text(
        "🔒 قفل لینک فعال شد"
    )



async def unlock_links(update, context):

    cfg = get_chat(update.effective_chat.id)

    cfg["links"] = False

    data = load()
    data[str(update.effective_chat.id)] = cfg
    save(data)


    await update.message.reply_text(
        "🔓 قفل لینک خاموش شد"
    )



# افزودن کلمه

async def add_word(update, context):

    text = update.message.text

    word = text.replace(
        "افزودن کلمه",
        ""
    ).strip()


    if not word:

        await update.message.reply_text(
            "مثال:\nافزودن کلمه تست"
        )
        return



    data = load()

    cid = str(update.effective_chat.id)


    if cid not in data:

        data[cid] = {
            "bad_words": False,
            "words": False,
            "links": False,
            "list": []
        }


    if word not in data[cid]["list"]:

        data[cid]["list"].append(word)


    save(data)


    await update.message.reply_text(
        f"✅ کلمه ذخیره شد:\n{word}"
    )



# حذف کلمه

async def remove_word(update, context):

    text = update.message.text

    word = text.replace(
        "حذف کلمه",
        ""
    ).strip()


    data = load()

    cid = str(update.effective_chat.id)


    if cid in data:

        if word in data[cid]["list"]:

            data[cid]["list"].remove(word)


    save(data)


    await update.message.reply_text(
        f"🗑 حذف شد:\n{word}"
    )



# لیست

async def words_list(update, context):

    cfg = get_chat(
        update.effective_chat.id
    )


    if not cfg["list"]:

        await update.message.reply_text(
            "📋 لیست خالی است"
        )
        return



    await update.message.reply_text(
        "📋 کلمات فیلتر:\n\n"
        +
        "\n".join(cfg["list"])
    )



# بررسی پیام

async def check_locks(update, context):

    if not update.message:
        return


    if not update.message.text:
        return


    text = update.message.text


    cfg = get_chat(
        update.effective_chat.id
    )


    if cfg["words"]:

        for w in cfg["list"]:

            if w in text:

                await update.message.delete()

                return



    if cfg["links"]:

        if "http://" in text or "https://" in text:

            await update.message.delete()

            return
