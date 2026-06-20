import json
import os


FILE = "locks.json"



def load():

    if not os.path.exists(FILE):
        return {}

    with open(FILE,"r") as f:
        return json.load(f)



def save(data):

    with open(FILE,"w") as f:
        json.dump(data,f,indent=4)



def get_chat(chat_id):

    data = load()

    cid = str(chat_id)


    if cid not in data:

        data[cid] = {
            "bad_words": False,
            "words": False,
            "links": False,
            "forward": False,
            "username": False,
            "photo": False,
            "video": False,
            "file": False,
            "sticker": False
        }

        save(data)


    return data[cid]



async def toggle(update, key, status):

    chat = update.effective_chat

    data = get_chat(chat.id)

    data[key] = status

    all_data = load()

    all_data[str(chat.id)] = data

    save(all_data)



    await update.message.reply_text(
        "🔒 فعال شد" if status else "🔓 خاموش شد"
    )





async def lock_link(update,context):
    await toggle(update,"links",True)

async def unlock_link(update,context):
    await toggle(update,"links",False)



async def lock_forward(update,context):
    await toggle(update,"forward",True)

async def unlock_forward(update,context):
    await toggle(update,"forward",False)



async def lock_username(update,context):
    await toggle(update,"username",True)

async def unlock_username(update,context):
    await toggle(update,"username",False)



async def lock_photo(update,context):
    await toggle(update,"photo",True)

async def unlock_photo(update,context):
    await toggle(update,"photo",False)



async def lock_video(update,context):
    await toggle(update,"video",True)

async def unlock_video(update,context):
    await toggle(update,"video",False)



async def lock_file(update,context):
    await toggle(update,"file",True)

async def unlock_file(update,context):
    await toggle(update,"file",False)



async def lock_sticker(update,context):
    await toggle(update,"sticker",True)

async def unlock_sticker(update,context):
    await toggle(update,"sticker",False)






async def check_locks(update,context):

    if not update.message:
        return


    msg = update.message
    cfg = get_chat(update.effective_chat.id)



    if cfg["links"]:

        text = msg.text or ""

        if "http" in text or "t.me" in text:

            await msg.delete()
            return



    if cfg["username"]:

        if "@" in (msg.text or ""):

            await msg.delete()
            return




    if cfg["forward"]:

        if msg.forward_date:

            await msg.delete()
            return




    if cfg["photo"] and msg.photo:

        await msg.delete()
        return



    if cfg["video"] and msg.video:

        await msg.delete()
        return



    if cfg["file"] and msg.document:

        await msg.delete()
        return



    if cfg["sticker"] and msg.sticker:

        await msg.delete()
        return
