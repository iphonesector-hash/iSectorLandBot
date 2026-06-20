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
        "یکی از گزینه‌ها رو انتخاب کن 👇",
        reply_markup=keyboard
    )



async def help_cmd(update, context):

    await update.message.reply_text(
        "📌 راهنما\n\n"
        "/start شروع\n"
        "/profile پروفایل"
    )



async def profile_cmd(update, context):

    user = update.effective_user

    info = get_user(user)

    await update.message.reply_text(
        "👤 پروفایل\n\n"
        f"نام: {info['name']}\n"
        f"سطح: {info['level']}\n"
        f"امتیاز: {info['coins']}\n"
        f"VIP: {info['vip']}"
    )



async def menu_handler(update: Update, context):

    text = update.message.text


    if text == "🎮 سرگرمی":

        await update.message.reply_text(
            "🎮 سرگرمی:\n\n"
            "😂 جوک\n"
            "🧠 چیستان\n"
            "🎲 تاس\n"
            "🪙 شیر یا خط\n"
            "📌 فکت\n"
            "💪 انگیزشی\n"
            "💬 تکست"
        )


    elif text == "😂 جوک":

        add_coin(update.effective_user, 2)
        await update.message.reply_text(get_joke())


    elif text == "🧠 چیستان":

        add_coin(update.effective_user, 2)
        await update.message.reply_text(riddle())


    elif text == "🎲 تاس":

        add_coin(update.effective_user, 1)
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



    elif text == "🛡 مدیریت":

        await update.message.reply_text(
            "🛡 مدیریت:\n\n"
            "روی پیام کاربر ریپلای کن:\n\n"
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



    elif text == "🛠 کاربردی":

        await update.message.reply_text(
            "🛠 کاربردی:\n\n"
            "📅 تاریخ\n"
            "⏰ ساعت\n"
            "🌦 هوا\n"
            "💵 ارز\n"
            "🥇 طلا"
        )



    elif text == "📜 قوانین":

        await update.message.reply_text(
            "📜 قوانین:\n\n"
            "احترام الزامی است\n"
            "اسپم ممنوع\n"
            "تبلیغ ممنوع"
        )



    elif text == "🆘 پشتیبانی":

        await update.message.reply_text(
            "🆘 پشتیبانی iSectorLand"
        )



app = Application.builder().token(TOKEN).build()


app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("profile", profile_cmd))


# مدیریت گروه
app.add_handler(MessageHandler(filters.Regex("^اخطار$"), warn))
app.add_handler(MessageHandler(filters.Regex("^حذف اخطار$"), clear_warn))
app.add_handler(MessageHandler(filters.Regex("^بن$"), ban))
app.add_handler(MessageHandler(filters.Regex("^کیک$"), kick))
app.add_handler(MessageHandler(filters.Regex("^سکوت$"), mute))


# قفل ها
app.add_handler(MessageHandler(filters.Regex("^قفل فحش$"), lock_bad))
app.add_handler(MessageHandler(filters.Regex("^حذف قفل فحش$"), unlock_bad))
app.add_handler(MessageHandler(filters.Regex("^قفل کلمات$"), lock_words))
app.add_handler(MessageHandler(filters.Regex("^حذف قفل کلمات$"), unlock_words))


# منو
app.add_handler(
    MessageHandler(filters.TEXT, menu_handler)
)


# امنیت آخر اجرا شود
app.add_handler(
    MessageHandler(filters.TEXT, security)
)


print("🌻 iSectorLand Started")


app.run_polling()
