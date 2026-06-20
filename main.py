from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from modules.fun import *
from config import TOKEN, BOT_NAME


menu = [
    ["🎮 سرگرمی", "🛠 کاربردی"],
    ["🛡 مدیریت", "👤 پروفایل"],
    ["📜 قوانین", "⚙️ تنظیمات"],
    ["🆘 پشتیبانی"]
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = ReplyKeyboardMarkup(
        menu,
        resize_keyboard=True
    )

    await update.message.reply_text(
        f"{BOT_NAME}\n\n"
        "خوش اومدی 🌻\n"
        "یکی از گزینه‌ها رو انتخاب کن 👇",
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
        await update.message.reply_text(
            get_joke()
        )


    elif text == "🧠 چیستان":
        await update.message.reply_text(
            riddle()
        )


    elif text == "🎲 تاس":
        await update.message.reply_text(
            dice()
        )


    elif text == "🪙 شیر یا خط":
        await update.message.reply_text(
            coin()
        )


    elif text == "📌 فکت":
        await update.message.reply_text(
            get_fact()
        )


    elif text == "💪 انگیزشی":
        await update.message.reply_text(
            get_motive()
        )


    elif text == "💬 تکست":
        await update.message.reply_text(
            get_text()
        )


    elif text == "🛠 کاربردی":
        await update.message.reply_text(
            "🛠 ابزارها:\n\n"
            "📅 تاریخ\n"
            "⏰ ساعت\n"
            "🌦 هواشناسی\n"
            "💵 ارز\n"
            "🥇 طلا"
        )


    elif text == "🛡 مدیریت":
        await update.message.reply_text(
            "🛡 مدیریت گروه:\n\n"
            "بن\n"
            "اخطار\n"
            "سکوت\n"
            "قفل‌ها"
        )


    elif text == "📜 قوانین":
        await update.message.reply_text(
            "📜 قوانین:\n\n"
            "احترام به اعضا\n"
            "بدون اسپم\n"
            "بدون تبلیغ"
        )


    elif text == "🆘 پشتیبانی":
        await update.message.reply_text(
            "🆘 پشتیبانی iSectorLand"
        )


    else:
        await update.message.reply_text(
            "این بخش به زودی کامل میشه 🔥"
        )



app = Application.builder().token(TOKEN).build()


app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CommandHandler("help", help_cmd)
)

app.add_handler(
    MessageHandler(filters.TEXT, menu_handler)
)


print("🌻 iSectorLand Started")


app.run_polling()
