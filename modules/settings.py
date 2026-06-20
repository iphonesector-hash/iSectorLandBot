import json
import os

FILE = "group_settings.json"

default = {
    "spam": True,
    "link": True,
    "mention": True,
    "welcome": True,
    "welcome_msg": "👋 خوش اومدی {name} عزیز!"
}


def load():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get(chat_id):
    data = load()
    cid = str(chat_id)
    if cid not in data:
        data[cid] = default.copy()
        save(data)
    return data[cid]


def set_option(chat_id, key, value):
    data = load()
    cid = str(chat_id)
    if cid not in data:
        data[cid] = default.copy()
    data[cid][key] = value
    save(data)


async def is_admin(update, context):
    try:
        admins = await context.bot.get_chat_administrators(update.effective_chat.id)
        return any(a.user.id == update.effective_user.id for a in admins)
    except:
        return False


async def settings_handler(update, context):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ این بخش فقط برای ادمین‌هاست.")
        return

    chat_id = update.effective_chat.id
    cfg = get(chat_id)

    def status(val):
        return "✅ فعال" if val else "❌ غیرفعال"

    await update.message.reply_text(
        f"⚙️ <b>تنظیمات گروه</b>\n"
        f"{'─' * 25}\n"
        f"🚫 ضداسپم: {status(cfg.get('spam', True))}\n"
        f"🔗 فیلتر لینک: {status(cfg.get('link', True))}\n"
        f"🔔 فیلتر منشن: {status(cfg.get('mention', True))}\n"
        f"👋 خوش‌آمدگویی: {status(cfg.get('welcome', True))}\n\n"
        f"برای تغییر از دستورات زیر استفاده کن:\n"
        f"<code>/setwelcome پیام خوش‌آمد</code>\n"
        f"<code>/toggle spam</code>\n"
        f"<code>/toggle link</code>\n"
        f"<code>/toggle welcome</code>",
        parse_mode="HTML"
    )


async def toggle_setting(update, context):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ این دستور فقط برای ادمین‌هاست.")
        return

    if not context.args:
        await update.message.reply_text(
            "⚠️ بنویس کدوم تنظیم رو میخوای تغییر بدی.\n"
            "مثال: <code>/toggle spam</code>",
            parse_mode="HTML"
        )
        return

    key = context.args[0].lower()
    valid = ["spam", "link", "mention", "welcome"]

    if key not in valid:
        await update.message.reply_text(
            f"❌ گزینه معتبر نیست.\nگزینه‌های معتبر: {', '.join(valid)}"
        )
        return

    chat_id = update.effective_chat.id
    cfg = get(chat_id)
    current = cfg.get(key, True)
    set_option(chat_id, key, not current)

    status = "✅ فعال" if not current else "❌ غیرفعال"
    await update.message.reply_text(
        f"⚙️ تنظیم <b>{key}</b> شد: {status}",
        parse_mode="HTML"
    )


async def set_welcome(update, context):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ این دستور فقط برای ادمین‌هاست.")
        return

    if not context.args:
        await update.message.reply_text(
            "⚠️ متن خوش‌آمد رو بنویس.\n"
            "از {name} برای اسم کاربر استفاده کن.\n"
            "مثال: <code>/setwelcome سلام {name} خوش اومدی!</code>",
            parse_mode="HTML"
        )
        return

    msg = " ".join(context.args)
    set_option(update.effective_chat.id, "welcome_msg", msg)
    await update.message.reply_text(
        f"✅ پیام خوش‌آمد ذخیره شد:\n{msg}"
    )


async def welcome_new_member(update, context):
    """وقتی عضو جدید وارد میشه"""
    chat_id = update.effective_chat.id
    cfg = get(chat_id)

    if not cfg.get("welcome", True):
        return

    for member in update.message.new_chat_members:
        if member.is_bot:
            continue
        msg = cfg.get("welcome_msg", "👋 خوش اومدی {name} عزیز!")
        msg = msg.replace("{name}", f"<b>{member.first_name}</b>")
        await update.message.reply_text(msg, parse_mode="HTML")
