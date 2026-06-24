import json
import os

SETTINGS_FILE = "group_settings.json"
RULES_FILE = "group_rules.json"

default_settings = {
    "spam": False,
    "link": False,
    "mention": False,
    "welcome": True,
    "welcome_msg": "👋 خوش اومدی {name} عزیز به گروه!"
}

DEFAULT_RULES = (
    "📜 <b>قوانین گروه</b>\n"
    "━━━━━━━━━━━━━━━━━━\n\n"
    "۱. 🚫 توهین، فحاشی و بی‌احترامی ممنوع\n"
    "۲. 🔗 ارسال لینک تبلیغاتی بدون اجازه ممنوع\n"
    "۳. 📢 اسپم و پیام‌های تکراری ممنوع\n"
    "۴. 🔞 محتوای نامناسب ممنوع\n"
    "۵. 🤝 با دیگران محترمانه رفتار کن\n"
    "۶. 📌 پیام‌های غیرمرتبط ممنوع\n"
    "۷. 🔊 تبلیغ کانال/گروه بدون اجازه ممنوع\n\n"
    "⚠️ تخلف = اخطار → بن\n\n"
    "👮 ادمین‌ها: @sector_admin"
)


def load_settings():
    """بارگذاری تنظیمات"""
    if not os.path.exists(SETTINGS_FILE):
        return {}
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_settings(data):
    """ذخیره تنظیمات"""
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        pass


def get_settings(chat_id):
    """دریافت تنظیمات گروه"""
    data = load_settings()
    cid = str(chat_id)
    if cid not in data:
        data[cid] = default_settings.copy()
        save_settings(data)
    return data[cid]


def set_option(chat_id, key, value):
    """تنظیم گزینه"""
    data = load_settings()
    cid = str(chat_id)
    if cid not in data:
        data[cid] = default_settings.copy()
    data[cid][key] = value
    save_settings(data)


def load_rules():
    """بارگذاری قوانین"""
    if not os.path.exists(RULES_FILE):
        return {}
    try:
        with open(RULES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_rules(data):
    """ذخیره قوانین"""
    try:
        with open(RULES_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        pass


def get_rules(chat_id):
    """دریافت قوانین گروه"""
    data = load_rules()
    return data.get(str(chat_id), DEFAULT_RULES)


def set_rules(chat_id, text):
    """تنظیم قوانین"""
    data = load_rules()
    data[str(chat_id)] = text
    save_rules(data)


async def is_admin(update, context):
    """چک کردن ادمین بودن"""
    try:
        admins = await context.bot.get_chat_administrators(update.effective_chat.id)
        return any(a.user.id == update.effective_user.id for a in admins)
    except:
        return False


async def settings_handler(update, context):
    """نمایش تنظیمات"""
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ این بخش فقط برای ادمین‌هاست.")
        return

    chat_id = update.effective_chat.id
    cfg = get_settings(chat_id)

    def status(val):
        return "✅ فعال" if val else "❌ غیرفعال"

    await update.message.reply_text(
        f"⚙️ <b>تنظیمات گروه</b>\n"
        f"{'━' * 30}\n\n"
        f"🚫 ضد‌اسپم: {status(cfg.get('spam'))}\n"
        f"🔗 فیلتر لینک: {status(cfg.get('link'))}\n"
        f"🔔 فیلتر منشن: {status(cfg.get('mention'))}\n"
        f"👋 خوش‌آمدگویی: {status(cfg.get('welcome'))}\n\n"
        f"برای تغییر از دستورات زیر استفاده کن:\n"
        f"<code>/toggle spam</code>\n"
        f"<code>/toggle link</code>\n"
        f"<code>/toggle mention</code>\n"
        f"<code>/toggle welcome</code>",
        parse_mode="HTML"
    )


async def toggle_setting(update, context):
    """تبدیل وضعیت تنظیم"""
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ فقط ادمین‌ها.")
        return

    if not context.args:
        await update.message.reply_text(
            "مثال: <code>/toggle spam</code>",
            parse_mode="HTML"
        )
        return

    key = context.args[0].lower()
    valid = ["spam", "link", "mention", "welcome"]
    if key not in valid:
        await update.message.reply_text(
            f"❌ گزینه‌های معتبر: {', '.join(valid)}"
        )
        return

    chat_id = update.effective_chat.id
    cfg = get_settings(chat_id)
    new_val = not cfg.get(key, False)
    set_option(chat_id, key, new_val)
    
    status_text = "✅ فعال" if new_val else "❌ غیرفعال"
    
    labels = {
        "spam": "ضد‌اسپم",
        "link": "فیلتر لینک",
        "mention": "فیلتر منشن",
        "welcome": "خوش‌آمدگویی"
    }
    
    await update.message.reply_text(
        f"⚙️ {labels.get(key, key)} {status_text} شد.",
        parse_mode="HTML"
    )


async def set_welcome_msg(update, context):
    """تنظیم پیام خوش‌آمد"""
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ فقط ادمین‌ها.")
        return

    if not context.args:
        await update.message.reply_text(
            "مثال: <code>/setwelcome سلام {name} خوش اومدی!</code>",
            parse_mode="HTML"
        )
        return

    msg = " ".join(context.args)
    set_option(update.effective_chat.id, "welcome_msg", msg)
    await update.message.reply_text(
        f"✅ پیام خوش‌آمد ذخیره شد:\n{msg}"
    )


async def set_rules_handler(update, context):
    """تنظیم قوانین"""
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ فقط ادمین‌ها.")
        return

    if not context.args:
        await update.message.reply_text(
            "📜 برای تنظیم قوانین بنویس:\n"
            "<code>/setrules متن قوانین گروه</code>",
            parse_mode="HTML"
        )
        return

    text = " ".join(context.args)
    set_rules(update.effective_chat.id, text)
    await update.message.reply_text("✅ قوانین گروه ذخیره شد.")


async def rules_handler(update, context):
    """نمایش قوانین"""
    rules = get_rules(update.effective_chat.id)
    await update.message.reply_text(rules, parse_mode="HTML")


async def welcome_new_member(update, context):
    """خوش‌آمدگویی خودکار"""
    chat_id = update.effective_chat.id
    cfg = get_settings(chat_id)

    if not cfg.get("welcome", True):
        return

    for member in update.message.new_chat_members:
        if member.is_bot:
            continue
        msg = cfg.get("welcome_msg", "👋 خوش اومدی {name} عزیز!")
        msg = msg.replace("{name}", f"<b>{member.first_name}</b>")
        try:
            await update.message.reply_text(msg, parse_mode="HTML")
        except:
            await update.message.reply_text(f"👋 خوش اومدی {member.first_name}!")
