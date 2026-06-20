import os
import random

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")


menu = [
    ["🎮 سرگرمی", "😂 جوک"],
    ["🔮 فال", "🧠 چیستان"],
    ["🎲 بازی", "📜 قوانین"],
    ["🆘 پشتیبانی", "⚙️ تنظیمات"]
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(
        menu,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "🌻 به iSectorLand خوش اومدی 🤖\n\n"
        "یک گزینه انتخاب کن:",
        reply_markup=keyboard
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 دستورات:\n\n"
        "/start شروع\n"
        "/help راهنما\n\n"
        "یا از دکمه‌ها استفاده کن 👇"
    )


async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jokes = [
        "😂 چرا کامپیوتر رفت دکتر؟ چون ویروس گرفته بود!",
        "🤣 اینترنت قطع شد، مودم رفت افسردگی گرفت!",
        "😄 برنامه نویس چرا قهوه میخوره؟ چون باگ داره!"
    ]

    await update.message.reply_text(random.choice(jokes))


async def fal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔮 فال امروز:\n"
        "یه خبر خوب نزدیکته ✨"
    )


async def riddle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧠 چیستان:\n\n"
        "چیزی که دندان دارد ولی غذا نمی‌خورد؟"
        "\n\nجواب: شانه 😄"
    )


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(1,5)

    await update.message.reply_text(
        f"🎲 عدد شانس امروزت: {number}"
    )


async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📜 قوانین:\n\n"
        "1️⃣ احترام به اعضا\n"
        "2️⃣ اسپم ممنوع\n"
        "3️⃣ تبلیغ بدون اجازه ممنوع"
    )


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 پشتیبانی:\n"
        "برای کمک با ادمین تماس بگیر"
    )


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "😂 جوک":
        await joke(update, context)

    elif text == "🔮 فال":
        await fal(update, context)

    elif text == "🧠 چیستان":
        await riddle(update, context)

    elif text == "🎲 بازی":
        await game(update, context)

    elif text == "📜 قوانین":
        await rules(update, context)

    elif text == "🆘 پشتیبانی":
        await support(update, context)

    elif text == "🎮 سرگرمی":
        await update.message.reply_text(
            "🎮 بخش سرگرمی آماده است 😎"
        )

    elif text == "⚙️ تنظیمات":
        await update.message.reply_text(
            "⚙️ تنظیمات بزودی اضافه می‌شود"
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))

app.add_handler(
    MessageHandler(filters.TEXT, text_handler)
)

print("iSectorLand Bot Started")

app.run_polling()
