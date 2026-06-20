from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)

from modules.fun import (
    get_joke, get_fact, get_motive,
    get_text, dice, coin, riddle, rps, random_number
)
from modules.admin import (
    warn, clear_warning, warns, setwarnlimit,
    ban, unban, kick, mute, unmute,
    admin_text_handler, get_warn_limit
)
from modules.locks import (
    lock_link, unlock_link,
    lock_forward, unlock_forward,
    lock_username, unlock_username,
    lock_photo, unlock_photo,
    lock_video, unlock_video,
    lock_file, unlock_file,
    lock_sticker, unlock_sticker,
    check_locks
)
from modules.settings import (
    settings_handler, toggle_setting,
    set_welcome, welcome_new_member
)
from modules.profile import (
    get_user, add_message,
    profile_handler, leaderboard_handler
)
from modules.useful import (
    useful_handler, weather, translate,
    calculate, convert_unit
)
from config import TOKEN, BOT_NAME


# ─── منوها ─────────────────────────────────────────────
main_menu = [
    ["🎮 سرگرمی", "🛠 کاربردی"],
    ["🛡 مدیریت", "🔒 قفل‌ها"],
    ["👤 پروفایل", "🏆 رتبه‌بندی"],
    ["⚙️ تنظیمات", "🆘 پشتیبانی"]
]

fun_menu = [
    ["😂 جوک", "🧠 فکت"],
    ["💪 انگیزشی", "✨ متن"],
    ["🎲 تاس", "🪙 شیر یا خط"],
    ["🧩 چیستان", "✂️ سنگ کاغذ قیچی"],
    ["🔙 برگشت"]
]

useful_menu = [
    ["🌤 آب و هوا", "🌐 ترجمه"],
    ["🔢 حساب‌گر", "📐 تبدیل واحد"],
    ["🔙 برگشت"]
]

admin_menu = [
    ["⚠️ اخطار", "🧹 پاک اخطار", "📋 اخطارها"],
    ["🚫 بن", "✅ آنبن", "👢 کیک"],
    ["🔇 میوت", "🔊 آنمیوت"],
    ["⚙️ تنظیم حد اخطار"],
    ["🔙 برگشت"]
]

lock_menu = [
    ["قفل لینک", "حذف قفل لینک"],
    ["قفل فوروارد", "حذف قفل فوروارد"],
    ["قفل یوزرنیم", "حذف قفل یوزرنیم"],
    ["قفل عکس", "حذف قفل عکس"],
    ["قفل ویدیو", "حذف قفل ویدیو"],
    ["قفل فایل", "حذف قفل فایل"],
    ["قفل استیکر", "حذف قفل استیکر"],
    ["🔙 برگشت"]
]


def main_kb():
    return ReplyKeyboardMarkup(main_menu, resize_keyboard=True)

def fun_kb():
    return ReplyKeyboardMarkup(fun_menu, resize_keyboard=True)

def useful_kb():
    return ReplyKeyboardMarkup(useful_menu, resize_keyboard=True)

def admin_kb():
    return ReplyKeyboardMarkup(admin_menu, resize_keyboard=True)

def lock_kb():
    return ReplyKeyboardMarkup(lock_menu, resize_keyboard=True)


def clean(text):
    if not text:
        return ""
    for e in ["🎮","🛠","🛡","🔒","👤","📜","⚙️","🆘","🏆",
              "😂","🧠","💪","✨","🎲","🪙","🧩","✂️",
              "🌤","🌐","🔢","📐","⚠️","🔙","🚫","✅",
              "👢","🔇","🔊","📋","🧹"]:
        text = text.replace(e, "")
    return text.strip()


# ─── هندلرها ───────────────────────────────────────────

async def start(update: Update, context):
    user = update.effective_user
    get_user(user)
    await update.message.reply_text(
        f"{BOT_NAME}\n\n👋 خوش اومدی <b>{user.first_name}</b>!",
        reply_markup=main_kb(),
        parse_mode="HTML"
    )


async def calc_cmd(update: Update, context):
    if not context.args:
        await update.message.reply_text(
            "🔢 مثال: <code>/calc 25 * 4 + 10</code>",
            parse_mode="HTML"
        )
        return
    expr = " ".join(context.args)
    await update.message.reply_text(calculate(expr), parse_mode="HTML")


async def convert_cmd(update: Update, context):
    if not context.args:
        await update.message.reply_text(
            "📐 مثال: <code>/convert 100 km به m</code>",
            parse_mode="HTML"
        )
        return
    text = " ".join(context.args)
    await update.message.reply_text(convert_unit(text), parse_mode="HTML")


async def lock_handler(update: Update, context):
    text = update.message.text.strip()
    cmds = {
        "قفل لینک": lock_link, "حذف قفل لینک": unlock_link,
        "قفل فوروارد": lock_forward, "حذف قفل فوروارد": unlock_forward,
        "قفل یوزرنیم": lock_username, "حذف قفل یوزرنیم": unlock_username,
        "قفل عکس": lock_photo, "حذف قفل عکس": unlock_photo,
        "قفل ویدیو": lock_video, "حذف قفل ویدیو": unlock_video,
        "قفل فایل": lock_file, "حذف قفل فایل": unlock_file,
        "قفل استیکر": lock_sticker, "حذف قفل استیکر": unlock_sticker,
    }
    if text in cmds:
        await cmds[text](update, context)


# دستورات مدیریتی فارسی (دکمه‌ای)
ADMIN_COMMANDS = {
    "اخطار": warn,
    "پاک اخطار": clear_warning,
    "اخطارها": warns,
    "بن": ban,
    "آنبن": unban,
    "کیک": kick,
    "میوت": mute,
    "آنمیوت": unmute,
}


async def menu_handler(update: Update, context):
    text = update.message.text.strip()
    c = clean(text)

    # ─── دستورات مدیریتی فارسی ───
    if c in ADMIN_COMMANDS:
        context.args = []
        await ADMIN_COMMANDS[c](update, context)
        return

    # تنظیم حد اخطار
    if c == "تنظیم حد اخطار":
        limit = get_warn_limit(update.effective_chat.id)
        await update.message.reply_text(
            f"⚙️ <b>تنظیم حد اخطار</b>\n\n"
            f"حد فعلی: <b>{limit}</b> اخطار\n\n"
            f"برای تغییر بنویس:\n"
            f"<code>اخطار حد [عدد]</code>\n"
            f"مثال: <code>اخطار حد 5</code>",
            parse_mode="HTML"
        )
        return

    if text.startswith("اخطار حد"):
        await admin_text_handler(update, context)
        return

    # ─── منوی اصلی ───
    if c == "سرگرمی":
        await update.message.reply_text("🎮 بخش سرگرمی:", reply_markup=fun_kb())

    elif c == "کاربردی":
        await update.message.reply_text("🛠 بخش کاربردی:", reply_markup=useful_kb())

    elif c == "مدیریت":
        limit = get_warn_limit(update.effective_chat.id)
        await update.message.reply_text(
            f"🛡 <b>پنل مدیریت</b>\n"
            f"─────────────────\n"
            f"📌 روی پیام کاربر ریپلای کن، بعد دکمه مورد نظر رو بزن.\n\n"
            f"⚙️ حد اخطار فعلی: <b>{limit}</b>",
            reply_markup=admin_kb(),
            parse_mode="HTML"
        )

    elif c == "قفل‌ها":
        await update.message.reply_text("🔒 مدیریت قفل‌ها:", reply_markup=lock_kb())

    elif c == "پروفایل":
        await profile_handler(update, context)

    elif c == "رتبه‌بندی":
        await leaderboard_handler(update, context)

    elif c == "تنظیمات":
        await settings_handler(update, context)

    elif c == "پشتیبانی":
        await update.message.reply_text(
            "🆘 <b>پشتیبانی</b>\n\nبرای گزارش مشکل با سازنده تماس بگیر.",
            parse_mode="HTML"
        )

    elif c == "برگشت":
        await update.message.reply_text("🏠 منوی اصلی:", reply_markup=main_kb())

    # ─── منوی سرگرمی ───
    elif c == "جوک":
        await update.message.reply_text(get_joke())
    elif c == "فکت":
        await update.message.reply_text(get_fact())
    elif c == "انگیزشی":
        await update.message.reply_text(get_motive())
    elif c == "متن":
        await update.message.reply_text(get_text())
    elif c == "تاس":
        await update.message.reply_text(dice())
    elif c == "شیر یا خط":
        await update.message.reply_text(coin())
    elif c == "چیستان":
        await update.message.reply_text(riddle(), parse_mode="HTML")
    elif c == "سنگ کاغذ قیچی":
        await update.message.reply_text("✂️ بنویس: سنگ، کاغذ یا قیچی")
    elif c in ["سنگ", "کاغذ", "قیچی"]:
        await update.message.reply_text(rps(c))

    # ─── منوی کاربردی ───
    elif c in ["آب و هوا", "ترجمه", "حساب‌گر", "تبدیل واحد"]:
        await useful_handler(update, context)

    # ─── ردیابی پیام برای XP ───
    else:
        if update.effective_chat.type != "private":
            add_message(update.effective_user)


# ─── راه‌اندازی ───────────────────────────────────────
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("profile", profile_handler))
app.add_handler(CommandHandler("top", leaderboard_handler))
app.add_handler(CommandHandler("warn", warn))
app.add_handler(CommandHandler("clearwarn", clear_warning))
app.add_handler(CommandHandler("warns", warns))
app.add_handler(CommandHandler("setwarnlimit", setwarnlimit))
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("unban", unban))
app.add_handler(CommandHandler("kick", kick))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(CommandHandler("unmute", unmute))
app.add_handler(CommandHandler("weather", weather))
app.add_handler(CommandHandler("translate", translate))
app.add_handler(CommandHandler("calc", calc_cmd))
app.add_handler(CommandHandler("convert", convert_cmd))
app.add_handler(CommandHandler("toggle", toggle_setting))
app.add_handler(CommandHandler("setwelcome", set_welcome))

# قفل‌ها
app.add_handler(
    MessageHandler(
        filters.Regex(
            r"^(قفل لینک|حذف قفل لینک|قفل فوروارد|حذف قفل فوروارد|"
            r"قفل یوزرنیم|حذف قفل یوزرنیم|قفل عکس|حذف قفل عکس|"
            r"قفل ویدیو|حذف قفل ویدیو|قفل فایل|حذف قفل فایل|"
            r"قفل استیکر|حذف قفل استیکر)$"
        ),
        lock_handler
    ),
    group=0
)

# عضو جدید
app.add_handler(
    MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member),
    group=0
)

# منو
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler),
    group=1
)

# چک قفل‌ها
app.add_handler(
    MessageHandler(filters.ALL & ~filters.COMMAND, check_locks),
    group=2
)

print(f"✅ {BOT_NAME} Started!")
app.run_polling()
