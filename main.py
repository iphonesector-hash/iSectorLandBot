import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 ربات iSectorLand فعال شد!\n\n/help برای دستورات"
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 دستورات:\n/start\n/help\n/joke\n/fal\n/riddle\n\nمدیریت:\nاخطار"
    )


async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("😂 چرا کامپیوتر رفت دکتر؟ چون ویروس گرفته بود!")


async def fal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔮 فال امروز: یه اتفاق خوب در راهه 😉")


async def riddle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧠 چیستان: چیزی که پا داره ولی راه نمیره؟")


async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚠️ اخطار ثبت شد")


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("joke", joke))
app.add_handler(CommandHandler("fal", fal))
app.add_handler(CommandHandler("riddle", riddle))
app.add_handler(MessageHandler(filters.Regex("اخطار"), warn))

print("iSectorLand Bot Started")

app.run_polling()
