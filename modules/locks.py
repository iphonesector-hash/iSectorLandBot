import json
import os

FILE = "locks.json"

LOCK_NAMES = {
    "link": "لینک",
    "forward": "فوروارد",
    "username": "یوزرنیم",
    "photo": "عکس",
    "video": "ویدیو",
    "file": "فایل",
    "sticker": "استیکر",
    "gif": "گیف",
    "audio": "آهنگ",
    "text": "متن",
}

DEFAULT_LOCKS = {k: False for k in LOCK_NAMES}


def load() -> dict:
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data: dict):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_chat(chat_id) -> dict:
    data = load()
    cid = str(chat_id)
    if cid not in data:
        data[cid] = DEFAULT_LOCKS.copy()
        save(data)
    else:
        # اضافه کردن کلیدهای جدید به گروه‌های قدیمی
        changed = False
        for k, v in DEFAULT_LOCKS.items():
            if k not in data[cid]:
                data[cid][k] = v
                changed = True
        if changed:
            save(data)
    return data[cid]


async def is_admin(update, context) -> bool:
    try:
        admins = await context.bot.get_chat_administrators(update.effective_chat.id)
        return any(x.user.id == update.effective_user.id for x in admins)
    except Exception:
        return False


async def toggle(update, context, key: str, value: bool):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ این دستور فقط برای ادمین‌هاست.")
        return

    chat_id = update.effective_chat.id
    data = load()
    cid = str(chat_id)
    if cid not in data:
        data[cid] = DEFAULT_LOCKS.copy()
    data[cid][key] = value
    save(data)

    label = LOCK_NAMES.get(key, key)
    if value:
        await update.message.reply_text(f"🔒 قفل {label} فعال شد.")
    else:
        await update.message.reply_text(f"🔓 قفل {label} غیرفعال شد.")


async def unlock_all(update, context):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ این دستور فقط برای ادمین‌هاست.")
        return
    chat_id = update.effective_chat.id
    data = load()
    data[str(chat_id)] = DEFAULT_LOCKS.copy()
    save(data)
    await update.message.reply_text("🔓 همه قفل‌ها باز شدند.")


async def show_locks_status(update, context):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ این دستور فقط برای ادمین‌هاست.")
        return
    cfg = get_chat(update.effective_chat.id)
    lines = ["🔒 <b>وضعیت قفل‌های گروه:</b>\n"]
    for key, label in LOCK_NAMES.items():
        icon = "✅" if cfg.get(key) else "❌"
        lines.append(f"{icon} قفل {label}")
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")


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
async def lock_gif(update, context): await toggle(update, context, "gif", True)
async def unlock_gif(update, context): await toggle(update, context, "gif", False)
async def lock_audio(update, context): await toggle(update, context, "audio", True)
async def unlock_audio(update, context): await toggle(update, context, "audio", False)
async def lock_text(update, context): await toggle(update, context, "text", True)
async def unlock_text(update, context): await toggle(update, context, "text", False)


async def check_locks(update, context):
    if not update.message:
        return

    # چک null بودن کاربر (پیام‌های کانال)
    if not update.effective_user:
        return

    chat = update.effective_chat
    if not chat:
        return

    # فقط در گروه‌ها اعمال بشه
    if chat.type not in ["group", "supergroup"]:
        return

    # ادمین‌ها معاف
    try:
        admins = await context.bot.get_chat_administrators(chat.id)
        if any(a.user.id == update.effective_user.id for a in admins):
            return
    except Exception:
        return

    msg = update.message
    cfg = get_chat(chat.id)
    text = msg.text or msg.caption or ""

    async def delete_and_notify(reason: str):
        try:
            await msg.delete()
        except Exception:
            pass
        try:
            await context.bot.send_message(chat.id, f"🔒 {reason}")
        except Exception:
            pass

    if cfg.get("link") and ("http" in text or "t.me/" in text):
        await delete_and_notify("ارسال لینک در این گروه ممنوع است.")
        return

    if cfg.get("username") and "@" in text:
        await delete_and_notify("ذکر یوزرنیم در این گروه ممنوع است.")
        return

    if cfg.get("forward") and msg.forward_date:
        await delete_and_notify("فوروارد پیام در این گروه ممنوع است.")
        return

    if cfg.get("photo") and msg.photo:
        try:
            await msg.delete()
        except Exception:
            pass
        return

    if cfg.get("video") and msg.video:
        try:
            await msg.delete()
        except Exception:
            pass
        return

    if cfg.get("file") and msg.document:
        try:
            await msg.delete()
        except Exception:
            pass
        return

    if cfg.get("sticker") and msg.sticker:
        try:
            await msg.delete()
        except Exception:
            pass
        return

    if cfg.get("gif") and msg.animation:
        try:
            await msg.delete()
        except Exception:
            pass
        return

    if cfg.get("audio") and (msg.audio or msg.voice):
        try:
            await msg.delete()
        except Exception:
            pass
        return

    if cfg.get("text") and msg.text and not msg.photo and not msg.video:
        try:
            await msg.delete()
        except Exception:
            pass
        return
