import json
import os

FILE = "locks.json"


def load():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)  # باگ قبلی: json.load() بدون آرگومان بود


def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_chat(chat_id):
    data = load()
    cid = str(chat_id)
    if cid not in data:
        data[cid] = {
            "link": False,
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
    try:
        admins = await context.bot.get_chat_administrators(update.effective_chat.id)
        return any(x.user.id == update.effective_user.id for x in admins)
    except:
        return False


async def toggle(update, context, key, value):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ این دستور فقط برای ادمین‌هاست.")
        return

    chat_id = update.effective_chat.id
    data = load()
    cid = str(chat_id)

    if cid not in data:
        data[cid] = get_chat(chat_id)

    data[cid][key] = value
    save(data)

    names = {
        "link": "لینک",
        "forward": "فوروارد",
        "username": "یوزرنیم",
        "photo": "عکس",
        "video": "ویدیو",
        "file": "فایل",
        "sticker": "استیکر"
    }

    label = names.get(key, key)
    if value:
        await update.message.reply_text(f"🔒 قفل {label} فعال شد.")
    else:
        await update.message.reply_text(f"🔓 قفل {label} غیرفعال شد.")


async def lock_link(update, context): await toggle(update, context, "link", True)
async def unlock_link(update, context): await toggle(update, context, "link", False)

async def lock_forward(update, context): await toggle(update, context, "forward", True)
async def unlock_forward(update, context): await toggle(update, context, "forward", False)

async def lock_username(update, context): await toggle(update, context, "username", True)
async def unlock_username(update, context): await toggle(update, context, "username", False)

async def lock_photo(update, context): await toggle(update, context, "photo", True)
async def unlock_photo(update, context): await toggle(update, context, "photo", False)

async def lock_video(update, context): await toggle(update, context, "video", True)
async def unlock_video(update, context): await toggle(update, context, "video", False)

async def lock_file(update, context): await toggle(update, context, "file", True)
async def unlock_file(update, context): await toggle(update, context, "file", False)

async def lock_sticker(update, context): await toggle(update, context, "sticker", True)
async def unlock_sticker(update, context): await toggle(update, context, "sticker", False)


async def check_locks(update, context):
    if not update.message:
        return

    # ادمین‌ها معاف از قفل‌ها هستن
    try:
        admins = await context.bot.get_chat_administrators(update.effective_chat.id)
        if any(a.user.id == update.effective_user.id for a in admins):
            return
    except:
        pass

    msg = update.message
    cfg = get_chat(update.effective_chat.id)
    text = msg.text or msg.caption or ""

    if cfg["link"] and ("http" in text or "t.me/" in text):
        await msg.delete()
        await context.bot.send_message(
            update.effective_chat.id,
            f"🔒 ارسال لینک در این گروه ممنوع است."
        )
        return

    if cfg["username"] and "@" in text:
        await msg.delete()
        await context.bot.send_message(
            update.effective_chat.id,
            f"🔒 ذکر یوزرنیم در این گروه ممنوع است."
        )
        return

    if cfg["forward"] and msg.forward_date:
        await msg.delete()
        await context.bot.send_message(
            update.effective_chat.id,
            f"🔒 فوروارد پیام در این گروه ممنوع است."
        )
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
