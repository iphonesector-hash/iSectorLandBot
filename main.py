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



async def start(update, context):

    get_user(update.effective_user)

    await update.message.reply_text(
        f"{BOT_NAME}\n\n🌻 خوش اومدی",
        reply_markup=ReplyKeyboardMarkup(
            menu,
            resize_keyboard=True
        )
    )



async def help_cmd(update, context):

    await update.message.reply_text(
        "📌 راهنما\n/start\n/profile"
    )



async def profile_cmd(update, context):

    info = get_user(update.effective_user)

    await update.message.reply_text(
        "👤 پروفایل\n\n"
        f"نام: {info['name']}\n"
        f"سطح: {info['level']}\n"
        f"سکه: {info['coins']}"
    )



async def menu_handler(update, context):

    text = update.message.text


    if text == "🎮 سرگرمی":

        await update.message.reply_text(
            "🎮 سرگرمی:\n\n"
            "😂 جوک\n"
            "🧠 چیستان\n"
            "🎲 تاس\n"
            "🪙 شیر یا خط"
        )


    elif text == "😂 جوک":

        await update.message.reply_text(get_joke())


    elif text == "🧠 چیستان":

        await update.message.reply_text(riddle())


    elif text == "🎲 تاس":

        await update.message.reply_text(dice())


    elif text == "👤 پروفایل":

        await profile_cmd(update, context)



    elif text == "🛡 مدیریت":

        await update.message.reply_text(
            "🛡 مدیریت:\n\n"
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
            "افزودن فحش تست\n"
            "حذف فحش تست\n"
            "لیست فحش\n\n"
            "قفل کلمات\n"
            "افزودن کلمه تست\n"
            "لیست کلمات"
        )



    elif text == "📜 قوانین":

        await update.message.reply_text(
            "📜 قوانین:\nاحترام + بدون اسپم"
        )



    elif text == "🆘 پشتیبانی":

        await update.message.reply_text(
            "🆘 پشتیبانی iSectorLand"
        )





app = Application.builder().token(TOKEN).build()



app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("profile", profile_cmd))



# قفل فحش

app.add_handler(
    MessageHandler(
        filters.Regex("^قفل فحش$"),
        lock_bad
    )
)

app.add_handler(
    MessageHandler(
        filters.Regex("^حذف قفل فحش$"),
        unlock_bad
    )
)


app.add_handler(
    MessageHandler(
        filters.Regex("^افزودن فحش (.+)$"),
        add_bad
    )
)


app.add_handler(
    MessageHandler(
        filters.Regex("^حذف فحش (.+)$"),
        remove_bad
    )
)


app.add_handler(
    MessageHandler(
        filters.Regex("^لیست فحش$"),
        bad_list
    )
)



# قفل کلمات

app.add_handler(
    MessageHandler(
        filters.Regex("^قفل کلمات$"),
        lock_words
    )
)

app.add_handler(
    MessageHandler(
        filters.Regex("^حذف قفل کلمات$"),
        unlock_words
    )
)


app.add_handler(
    MessageHandler(
        filters.Regex("^افزودن کلمه (.+)$"),
        add_word
    )
)


app.add_handler(
    MessageHandler(
        filters.Regex("^حذف کلمه (.+)$"),
        remove_word
    )
)


app.add_handler(
    MessageHandler(
        filters.Regex("^لیست کلمات$"),
        words_list
    )
)



# لینک

app.add_handler(
    MessageHandler(
        filters.Regex("^قفل لینک$"),
        lock_links
    )
)

app.add_handler(
    MessageHandler(
        filters.Regex("^حذف قفل لینک$"),
        unlock_links
    )
)



# مدیریت

app.add_handler(MessageHandler(filters.Regex("^اخطار$"), warn))
app.add_handler(MessageHandler(filters.Regex("^بن$"), ban))
app.add_handler(MessageHandler(filters.Regex("^کیک$"), kick))
app.add_handler(MessageHandler(filters.Regex("^سکوت$"), mute))



# بررسی قفل‌ها آخر اجرا شود

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        check_locks
    ),
    group=2
)



# منو

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        menu_handler
    ),
    group=1
)



print("🌻 iSectorLand Started")

app.run_polling()
