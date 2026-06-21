import json
import os

FILE = "group_settings.json"
RULES_FILE = "group_rules.json"

default = {
    "spam": False,
    "link": False,
    "mention": False,
    "welcome": True,
    "welcome_msg": "👋 خوش اومدی {name} عزیز به گروه!"
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


# ─── قوانین ────────────────────────────────────────────
def load_rules():
    if not os.path.exists(RULES_FILE):
        return {}
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rules(data):
    with open(RULES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


DEFAULT_RULES = (
    "📜 <b>قوانین گروه</b>\n"
    "━━━━━━━━━━━━━━━━━━\n\n"
    "۱. 🚫 توهین، فحاشی و بی‌احترامی ممنوع\n"
    "۲. 🔗 ارسال لینک تبلیغاتی بدون اجازه ممنوع\n"
    "۳. 📢 اسپم و پیام‌های تکراری ممنوع\n"
    "۴. 🔞 محتوای نامناسب ممنوع\n"
    "۵. 🤝 با دیگران محترمانه رفتار کن\n"
    "۶. 📌 پیام‌های غیرمرتبط با موضوع گروه ممنوع\n"
    "۷. 🔊 تبلیغ کانال یا گروه دیگه بدون اجازه ادمین ممنوع\n\n"
    "⚠️ تخلف از قوانین = اخطار و در صورت تکرار بن\n\n"
    "👮 ادمین‌ها: @sector_ad"
)


def get_rules(chat_id):
    data = load_rules()
    return data.get(str(chat_id), DEFAULT_RULES)


def set_rules(chat_id, text):
    data = load_rules()
    data[str(chat_id)] = text
    save_rules(data)


# ─── چک ادمین ──────────────────────────────────────────
async def is_admin(update, context):
    try:
        admins = await context.bot.get_chat_administrators(update.effective_chat.id)
        return any(a.user.id == update.effective_user.id for a in admins)
    except:
        return False


# ─── نمایش تنظیمات (متنی، بدون دکمه اینلاین) ──────────
async def settings_handler(update, context):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ این بخش فقط برای ادمین‌هاست.")
        return

    chat_id = update.effective_chat.id
    cfg = get(chat_id)

    def st(val):
        return "✅ فعال" if val else "❌ غیرفعال"

    await update.message.reply_text(
        f"⚙️ <b>تنظیمات گروه</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"🚫 ضداسپم: {st(cfg.get('spam'))}\n"
        f"🔗 فیلتر لینک: {st(cfg.get('link'))}\n"
        f"🔔 فیلتر منشن: {st(cfg.get('mention'))}\n"
        f"👋 خوش‌آمدگویی: {st(cfg.get('welcome'))}\n\n"
        f"برای تغییر هر گزینه روی دکمه‌های زیر بزن:",
        reply_markup=settings_kb(cfg),
        parse_mode="HTML"
    )


from telegram import ReplyKeyboardMarkup

def settings_kb(cfg=None):
    def lbl(key, on_text, off_text):
        if cfg and cfg.get(key):
            return f"🔴 {on_text} خاموش کن"
        return f"🟢 {on_text} روشن کن"

    return ReplyKeyboardMarkup([
        [lbl("spam", "ضداسپم", ""), lbl("link", "فیلتر لینک", "")],
        [lbl("mention", "فیلتر منشن", ""), lbl("welcome", "خوش‌آمدگویی", "")],
        ["✏️ تغییر پیام خوش‌آمد", "📜 قوانین گروه"],
        ["🔙 برگشت"]
    ], resize_keyboard=True)


# ─── هندلر دکمه‌های تنظیمات ────────────────────────────
async def settings_button_handler(update, context):
    text = update.message.text.strip()

    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ فقط ادمین‌ها.")
        return

    chat_id = update.effective_chat.id
    cfg = get(chat_id)

    toggle_map = {
        "ضداسپم": "spam",
        "فیلتر لینک": "link",
        "فیلتر منشن": "mention",
        "خوش‌آمدگویی": "welcome",
    }

    for label, key in toggle_map.items():
        if label in text:
            new_val = not cfg.get(key, False)
            set_option(chat_id, key, new_val)
            cfg = get(chat_id)
            st = "✅ فعال" if new_val else "❌ غیرفعال"
            await update.message.reply_text(
                f"⚙️ {label} {st} شد.",
                reply_markup=settings_kb(cfg),
                parse_mode="HTML"
            )
            return

    if text == "✏️ تغییر پیام خوش‌آمد":
        await update.message.reply_text(
            "✏️ <b>تغییر پیام خوش‌آمدگویی</b>\n\n"
            "دستور زیر رو با متن دلخواهت بفرست:\n"
            "<code>/setwelcome سلام {name} خوش اومدی!</code>\n\n"
            "از <code>{name}</code> برای اسم کاربر استفاده کن.",
            parse_mode="HTML"
        )
        return

    if text == "📜 قوانین گروه":
        rules = get_rules(chat_id)
        await update.message.reply_text(
            rules + "\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "برای تغییر قوانین:\n"
            "<code>/setrules متن قوانین</code>",
            parse_mode="HTML"
        )
        return


# ─── دستور /setrules ───────────────────────────────────
async def set_rules_handler(update, context):
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


# ─── دستور /rules ──────────────────────────────────────
async def rules_handler(update, context):
    rules = get_rules(update.effective_chat.id)
    await update.message.reply_text(rules, parse_mode="HTML")


# ─── دستور /toggle ─────────────────────────────────────
async def toggle_setting(update, context):
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
        await update.message.reply_text(f"❌ گزینه‌های معتبر: {', '.join(valid)}")
        return

    chat_id = update.effective_chat.id
    cfg = get(chat_id)
    new_val = not cfg.get(key, False)
    set_option(chat_id, key, new_val)
    st = "✅ فعال" if new_val else "❌ غیرفعال"
    await update.message.reply_text(f"⚙️ {key} {st} شد.", parse_mode="HTML")


# ─── دستور /setwelcome ─────────────────────────────────
async def set_welcome(update, context):
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
    await update.message.reply_text(f"✅ پیام خوش‌آمد ذخیره شد:\n{msg}")


# ─── خوش‌آمدگویی خودکار ────────────────────────────────
async def welcome_new_member(update, context):
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
