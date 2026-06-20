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
from modules.settings import *
from modules.profile import *

from config import TOKEN, BOT_NAME



menu = [
    ["🎮 سرگرمی", "🛠 کاربردی"],
    ["🛡 مدیریت", "🔒 قفل‌ها"],
    ["👤 پروفایل", "🏆 رتبه‌بندی"],
    ["⚙️ تنظیمات", "📜 قوانین"],
    ["🆘 پشتیبانی"]
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



async def profile(update, context):

    user = update.effective_user

    info = get_user(user)


    await update.message.reply_text(
        "👤 پروفایل شما\n\n"
        f"🧑 نام: {info['name']}\n"
        f"⭐ سطح: {info['level']}\n"
        f"🪙 امتیاز: {info['coins']}\n"
        f"👑 VIP: {info['vip']}"
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
        add_coin(update.effective_user,2)
        await update.message.reply_text(get_joke())


    elif text == "🧠 چیستان":
        add_coin(update.effective_user,2)
        await update.message.reply_text(riddle())


    elif text == "🎲 تاس":
        add_coin(update.effective_user,1)
        await update.message.reply_text(dice())


    elif text == "🪙 شیر یا خط":
        add_coin(update.effective_user,1)
        await update.message.reply_text(coin())


    elif text == "📌 فکت":
        await update.message.reply_text(get_fact())


    elif text == "💪 انگیزشی":
        await update.message.reply_text(get_motive())


    elif text == "💬 تکست":
        await update.message.reply_text(get_text())



    elif text == "👤 پروفایل":

        await profile(update,context)



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
            "🛡 مدیریت:\n\n"
            "ریپلای کن:\n"
            "اخطار\n"
            "بن\n"
            "کیک\n"
            "سکوت"
        )



    elif text == "🔒 قفل‌ها":

        await update.message.reply_text(
            "🔒 قفل‌ها:\n\n"
            "قفل فحش\n"
            "حذف قفل فحش\n"
            "قفل کلمات\n"
            "حذف قفل کلمات\n"
            "قفل لینک"
        )



    elif text == "⚙️ تنظیمات":

        cfg = get(update.effective_chat.id)

        await update.message.reply_text(
            "⚙️ تنظیمات\n\n"
            f"ضد اسپم: {cfg['spam']}\n"
            f"لینک: {cfg['link']}"
        )



    elif text == "📜 قوانین":

        await update.message.reply_text(
            "📜 قوانین:\n\n"
            "1 احترام\n"
            "2 بدون اسپم\n"
            "3 بدون تبلیغ"
        )



    elif text == "🆘 پشتیبانی":

        await update.message.reply_text(
            "🆘 پشتیبانی iSectorLand"
        )



app = Application.builder().token(TOKEN).build()



app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("help",help_cmd))
app.add_handler(CommandHandler("profile",profile))


# مدیریت
app.add_handler(MessageHandler(filters.Regex("^اخطار$"),warn))
app.add_handler(MessageHandler(filters.Regex("^پاک کردن اخطار$"),clear_warn))
app.add_handler(MessageHandler(filters.Regex("^بن$"),ban))
app.add_handler(MessageHandler(filters.Regex("^کیک$"),kick))
app.add_handler(MessageHandler(filters.Regex("^سکوت$"),mute))



# قفل‌ها
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        check_locks
    )
)


app.add_handler(MessageHandler(filters.Regex("^قفل فحش$"),lock_bad))
app.add_handler(MessageHandler(filters.Regex("^حذف قفل فحش$"),unlock_bad))
app.add_handler(MessageHandler(filters.Regex("^قفل کلمات$"),lock_words))
app.add_handler(MessageHandler(filters.Regex("^حذف قفل کلمات$"),unlock_words))
app.add_handler(MessageHandler(filters.Regex("^قفل لینک$"),lock_links))
app.add_handler(MessageHandler(filters.Regex("^حذف قفل لینک$"),unlock_links))



app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        menu_handler
    )
)



print("🌻 iSectorLand Started")


app.run_polling()
