from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from modules.fun import *
from modules.admin import *
from modules.locks import *
from modules.security import *
from modules.settings import *
from modules.profile import *
from modules.warnings import *

from config import TOKEN, BOT_NAME


menu = [
    ["🎮 سرگرمی", "🛠 کاربردی"],
    ["🛡 مدیریت", "🔒 قفل‌ها"],
    ["👤 پروفایل", "⚙️ تنظیمات"],
    ["📜 قوانین", "🆘 پشتیبانی"]
]


async def start(update: Update, context):

    get_user(update.effective_user)

    keyboard = ReplyKeyboardMarkup(
        menu,
        resize_keyboard=True
    )

    await update.message.reply_text(
        f"{BOT_NAME}\n\n"
        "🌻 خوش اومدی\n"
        "یک گزینه انتخاب کن 👇",
        reply_markup=keyboard
    )


async def help_cmd(update, context):

    await update.message.reply_text(
        "📌 راهنما\n\n"
        "/start شروع\n"
        "/profile پروفایل"
    )


async def profile_cmd(update, context):

    info = get_user(update.effective_user)

    await update.message.reply_text(
        "👤 پروفایل\n\n"
        f"🧑 نام: {info['name']}\n"
        f"⭐ سطح: {info['level']}\n"
        f"🪙 امتیاز: {info['coins']}"
    )


async def menu_handler(update, context):

    text = update.message.text


    if text == "🎮 سرگرمی":
        await update.message.reply_text(
            "🎮 سرگرمی‌ها:\n\n"
            "😂 جوک\n"
            "🧠 چیستان\n"
            "🎲 تاس\n"
            "🪙 شیر یا خط\n"
            "📌 فکت\n"
            "💪 انگیزشی\n"
            "💬 تکست"
        )


    elif text == "😂 جوک":
        await update.message.reply_text(get_joke())


    elif text == "🧠 چیستان":
        await update.message.reply_text(riddle())


    elif text == "🎲 تاس":
        await update.message.reply_text(dice())


    elif text == "🪙 شیر یا خط":
        await update.message.reply_text(coin())


    elif text == "📌 فکت":
        await update.message.reply_text(get_fact())


    elif text == "💪 انگیزشی":
        await update.message.reply_text(get_motive())


    elif text == "💬 تکست":
        await update.message.reply_text(get_text())


    elif text == "👤 پروفایل":
        await profile_cmd(update, context)


    elif text == "🛠 کاربردی":
        await update.message.reply_text(
            "🛠 کاربردی:\n\n"
            "📅 تاریخ\n"
            "⏰ ساعت\n"
            "🌦 هواشناسی\n"
            "💵 ارز\n"
            "🥇 طلا\n"
            "🚗 خودرو"
        )


    elif text == "🛡 مدیریت":
        await update.message.reply_text(
            "🛡 مدیریت گروه:\n\n"
            "ریپلای کن:\n"
            "⚠️ اخطار\n"
            "🚫 بن\n"
            "👢 کیک\n"
            "🔇 سکوت"
        )


    elif text == "🔒 قفل‌ها":
        await update.message.reply_text(
            "🔒 قفل‌ها:\n\n"
            "قفل فحش\n"
            "حذف قفل فحش\n"
            "قفل کلمات\n"
            "حذف قفل کلمات"
        )


    elif text == "⚙️ تنظیمات":
        await update.message.reply_text(
            "⚙️ تنظیمات آماده شد"
        )


    elif text == "📜 قوانین":
        await update.message.reply_text(
            "📜 قوانین:\n"
            "احترام\n"
            "بدون اسپم\n"
            "بدون تبلیغ"
        )


    elif text == "🆘 پشتیبانی":
        await update.message.reply_text(
            "🆘 پشتیبانی iSectorLand"
        )



app = Application.builder().token(TOKEN).build()


app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("profile", profile_cmd))


# مدیریت
app.add_handler(MessageHandler(filters.Regex("^اخطار$"), warn))
app.add_handler(MessageHandler(filters.Regex("^حذف اخطار$"), clear_warn))
app.add_handler(MessageHandler(filters.Regex("^بن$"), ban))
app.add_handler(MessageHandler(filters.Regex("^کیک$"), kick))
app.add_handler(MessageHandler(filters.Regex("^سکوت$"), mute))


# قفل
app.add_handler(MessageHandler(filters.Regex("^قفل فحش$"), lock_bad))
app.add_handler(MessageHandler(filters.Regex("^حذف قفل فحش$"), unlock_bad))
app.add_handler(MessageHandler(filters.Regex("^قفل کلمات$"), lock_words))
app.add_handler(MessageHandler(filters.Regex("^حذف قفل کلمات$"), unlock_words))


# منو (اصلی)
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        menu_handler
    )
)


# امنیت آخر
app.add_handler(
    MessageHandler(
        filters.TEXT,
        security
    )
)


print("🌻 iSectorLand Started")

app.run_polling()
