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
from config import TOKEN, BOT_NAME


menu = [
    ["🎮 سرگرمی", "🛠 کاربردی"],
    ["🛡 مدیریت", "🔒 قفل‌ها"],
    ["📜 قوانین", "⚙️ تنظیمات"],
    ["🆘 پشتیبانی"]
]


async def start(update: Update, context):

    keyboard = ReplyKeyboardMarkup(
        menu,
        resize_keyboard=True
    )

    await update.message.reply_text(
        f"{BOT_NAME}\n\n"
        "خوش اومدی 🌻\n"
        "یک گزینه انتخاب کن 👇",
        reply_markup=keyboard
    )


async def help_cmd(update: Update, context):

    await update.message.reply_text(
        "📌 راهنما\n\n"
        "/start شروع\n"
        "/help راهنما"
    )


async def menu_handler(update: Update, context):

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


    elif text == "🛠 کاربردی":

        await update.message.reply_text(
            "🛠 کاربردی:\n\n"
            "📅 تاریخ\n"
            "⏰ ساعت\n"
            "🌦 هواشناسی\n"
            "💵 قیمت ارز\n"
            "🥇 قیمت طلا\n"
            "🚗 قیمت خودرو"
        )


    elif text == "🛡 مدیریت":

        await update.message.reply_text(
            "🛡 مدیریت گروه:\n\n"
            "روی پیام ریپلای کن:\n\n"
            "⚠️ اخطار\n"
            "🧹 حذف اخطار\n"
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


    elif text == "📜 قوانین":

        await update.message.reply_text(
            "📜 قوانین:\n\n"
            "1️⃣ احترام\n"
            "2️⃣ بدون اسپم\n"
            "3️⃣ بدون تبلیغ"
        )


    elif text == "🆘 پشتیبانی":

        await update.message.reply_text(
            "🆘 پشتیبانی iSectorLand"
        )



app = Application.builder().token(TOKEN).build()


app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CommandHandler("help", help_cmd)
)


# مدیریت
app.add_handler(
    MessageHandler(filters.Regex("^اخطار$"), warn)
)

app.add_handler(
    MessageHandler(filters.Regex("^حذف اخطار$"), clear_warn)
)

app.add_handler(
    MessageHandler(filters.Regex("^بن$"), ban)
)

app.add_handler(
    MessageHandler(filters.Regex("^کیک$"), kick)
)

app.add_handler(
    MessageHandler(filters.Regex("^سکوت$"), mute)
)


# قفل ها
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        check_message
    )
)


app.add_handler(
    MessageHandler(filters.Regex("^قفل فحش$"), lock_bad)
)

app.add_handler(
    MessageHandler(filters.Regex("^حذف قفل فحش$"), unlock_bad)
)

app.add_handler(
    MessageHandler(filters.Regex("^قفل کلمات$"), lock_words)
)

app.add_handler(
    MessageHandler(filters.Regex("^حذف قفل کلمات$"), unlock_words)
)


app.add_handler(
    MessageHandler(
        filters.TEXT,
        menu_handler
    )
)


print("🌻 iSectorLand Started")


app.run_polling()
