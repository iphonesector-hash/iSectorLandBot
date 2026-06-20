import json
import os


FILE = "locks.json"



def load():

    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r") as f:
        return json.load()



def save(data):

    with open(FILE, "w") as f:
        json.dump(
            data,
            f,
            indent=4
        )



def get_chat(chat_id):

    data = load()

    cid = str(chat_id)

    if cid not in data:

        data[cid] = {
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



async def is_admin(update, context):

    admins = await context.bot.get_chat_administrators(
        update.effective_chat.id
    )

    for admin in admins:
        if admin.user.id == update.effective_user.id:
            return True

    return False



async def toggle(update, context, key, value):

    if not await is_admin(update, context):

        await update.message.reply_text(
            "⛔ فقط ادمین‌ها اجازه تغییر قفل دارند"
        )

        return


    chat = update.effective_chat

    data = get_chat(chat.id)

    data[key] = value


    all_data = load()

    all_data[str(chat.id)] = data

    save(all_data)



    await update.message.reply_text(
        "🔒 قفل فعال شد"
        if value
        else
        "🔓 قفل خاموش شد"
    )




async def lock_link(update,context):
    await toggle(update,context,"links",True)

async def unlock_link(update,context):
    await toggle(update,context,"links",False)



async def lock_forward(update,context):
    await toggle(update,context,"forward",True)

async def unlock_forward(update,context):
    await toggle(update,context,"forward",False)



async def lock_username(update,context):
    await toggle(update,context,"username",True)

async def unlock_username(update,context):
    await toggle(update,context,"username",False)



async def lock_photo(update,context):
    await toggle(update,context,"photo",True)

async def unlock_photo(update,context):
    await toggle(update,context,"photo",False)



async def lock_video(update,context):
    await toggle(update,context,"video",True)

async def unlock_video(update,context):
    await toggle(update,context,"video",False)



async def lock_file(update,context):
    await toggle(update,context,"file",True)

async def unlock_file(update,context):
    await toggle(update,context,"file",False)



async def lock_sticker(update,context):
    await toggle(update,context,"sticker",True)

async def unlock_sticker(update,context):
    await toggle(update,context,"sticker",False)




async def check_locks(update,context):

    if not update.message:
        return


    msg = update.message

    cfg = get_chat(
        update.effective_chat.id
    )



    if cfg.get("links"):

        text = msg.text or ""

        if "http" in text or "t.me" in text:

            await msg.delete()
            return



    if cfg.get("username"):

        if "@" in (msg.text or ""):

            await msg.delete()
            return



    if cfg.get("forward"):

        if msg.forward_date:

            await msg.delete()
            return



    if cfg.get("photo") and msg.photo:

        await msg.delete()
        return



    if cfg.get("video") and msg.video:

        await msg.delete()
        return



    if cfg.get("file") and msg.document:

        await msg.delete()
        return



    if cfg.get("sticker") and msg.sticker:

        await msg.delete()
        return
