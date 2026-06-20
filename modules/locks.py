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
            "list": [],
            "bad_list": []
        }

        save(data)


    return data[cid]



def save_chat(chat_id, cfg):

    data = load()

    data[str(chat_id)] = cfg

    save(data)



# قفل فحش

async def lock_bad(update, context):

    cfg = get_chat(update.effective_chat.id)

    cfg["bad_words"] = True

    save_chat(update.effective_chat.id, cfg)

    await update.message.reply_text(
        "🔒 قفل فحش فعال شد"
    )



async def unlock_bad(update, context):

    cfg = get_chat(update.effective_chat.id)

    cfg["bad_words"] = False

    save_chat(update.effective_chat.id, cfg)

    await update.message.reply_text(
        "🔓 قفل فحش خاموش شد"
    )



# افزودن فحش

async def add_bad(update, context):

    text = update.message.text

    word = text.replace(
        "افزودن فحش",
        ""
    ).strip()


    if not word:
        return


    cfg = get_chat(update.effective_chat.id)


    if word not in cfg["bad_list"]:

        cfg["bad_list"].append(word)


    save_chat(update.effective_chat.id, cfg)


    await update.message.reply_text(
        f"✅ فحش ذخیره شد:\n{word}"
    )



async def remove_bad(update, context):

    text = update.message.text

    word = text.replace(
        "حذف فحش",
        ""
    ).strip()


    cfg = get_chat(update.effective_chat.id)


    if word in cfg["bad_list"]:

        cfg["bad_list"].remove(word)


    save_chat(update.effective_chat.id, cfg)


    await update.message.reply_text(
        "🗑 حذف شد"
    )



async def bad_list(update, context):

    cfg = get_chat(update.effective_chat.id)


    if not cfg["bad_list"]:

        await update.message.reply_text(
            "📋 لیست فحش خالیه"
        )
        return


    await update.message.reply_text(
        "📋 فحش‌ها:\n\n" +
        "\n".join(cfg["bad_list"])
    )



# قفل کلمات

async def lock_words(update, context):

    cfg = get_chat(update.effective_chat.id)

    cfg["words"] = True

    save_chat(update.effective_chat.id, cfg)

    await update.message.reply_text(
        "🔒 قفل کلمات فعال شد"
    )



async def unlock_words(update, context):

    cfg = get_chat(update.effective_chat.id)

    cfg["words"] = False

    save_chat(update.effective_chat.id, cfg)

    await update.message.reply_text(
        "🔓 قفل کلمات خاموش شد"
    )



# افزودن کلمه

async def add_word(update, context):

    text = update.message.text

    word = text.replace(
        "افزودن کلمه",
        ""
    ).strip()


    if not word:
        return


    cfg = get_chat(update.effective_chat.id)


    if word not in cfg["list"]:

        cfg["list"].append(word)


    save_chat(update.effective_chat.id, cfg)


    await update.message.reply_text(
        f"✅ ذخیره شد:\n{word}"
    )



async def remove_word(update, context):

    text = update.message.text

    word = text.replace(
        "حذف کلمه",
        ""
    ).strip()


    cfg = get_chat(update.effective_chat.id)


    if word in cfg["list"]:

        cfg["list"].remove(word)


    save_chat(update.effective_chat.id, cfg)


    await update.message.reply_text(
        "🗑 حذف شد"
    )



async def words_list(update, context):

    cfg = get_chat(update.effective_chat.id)


    if not cfg["list"]:

        await update.message.reply_text(
            "📋 لیست خالی است"
        )
        return


    await update.message.reply_text(
        "📋 کلمات:\n\n" +
        "\n".join(cfg["list"])
    )



# لینک

async def lock_links(update, context):

    cfg = get_chat(update.effective_chat.id)

    cfg["links"] = True

    save_chat(update.effective_chat.id, cfg)

    await update.message.reply_text(
        "🔒 قفل لینک فعال شد"
    )



async def unlock_links(update, context):

    cfg = get_chat(update.effective_chat.id)

    cfg["links"] = False

    save_chat(update.effective_chat.id, cfg)

    await update.message.reply_text(
        "🔓 قفل لینک خاموش شد"
    )



# بررسی پیام

async def check_locks(update, context):

    if not update.message:
        return

    if not update.message.text:
        return


    text = update.message.text

    cfg = get_chat(update.effective_chat.id)



    if cfg["bad_words"]:

        for w in cfg["bad_list"]:

            if w in text:

                await update.message.delete()
                return



    if cfg["words"]:

        for w in cfg["list"]:

            if w in text:

                await update.message.delete()
                return



    if cfg["links"]:

        if "http://" in text or "https://" in text:

            await update.message.delete()
            return
