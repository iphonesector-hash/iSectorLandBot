from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)

from modules.fun import *
from modules.admin import *
from modules.locks import *
from modules.profile import *
from modules.settings import *

from config import TOKEN, BOT_NAME



menu = [
    ["🎮 سرگرمی", "🛠 کاربردی"],
    ["🛡 مدیریت", "🔒 قفل‌ها"],
    ["👤 پروفایل", "📜 قوانین"],
    ["⚙️ تنظیمات", "🆘 پشتیبانی"]
]



def clean_text(text):

    if not text:
        return ""

    emojis = [
        "🎮","🛠","🛡","🔒",
        "👤","📜","⚙️","🆘",
        "😂","🧠","🎲","🪙",
        "📌","💪","💬"
    ]

    for e in emojis:
        text = text.replace(e, "")

    return text.strip()



async def start(update, context):

    get_user(update.effective_user)

    await update.message.reply_text(
        f"{BOT_NAME}\n\n🌻 خوش اومدی",
        reply_markup=ReplyKeyboardMarkup(
            menu,
            resize_keyboard=True
        )
    )



async def profile_cmd(update, context):

    await profile(update, context)



async def menu_handler(update, context):

    if not update.message:
        return


    text = clean_text(
        update.message.text
    )


    if text == "سرگرمی":

        await update.message.reply_text(
            "🎮 سرگرمی:\n\n"
            "😂 جوک\n"
            "🧠 چیستان\n"
            "🎲 تاس\n"
            "🪙 شیر یا خط\n"
            "📌 فکت"
        )


    elif text == "جوک":

        await update.message.reply_text(
            get_joke()
        )


    elif text == "چیستان":

        await update.message.reply_text(
            riddle()
        )


    elif text == "تاس":

        await update.message.reply_text(
            dice()
        )


    elif text == "شیر یا خط":

        await update.message.reply_text(
            coin()
        )


    elif text == "فکت":

        await update.message.reply_text(
            get_fact()
        )


    elif text == "پروفایل":

        await profile_cmd(update, context)



    elif text == "مدیریت":

        await update.message.reply_text(
            "🛡 مدیریت:\n\n"
            "ریپلای کن:\n"
            "بن\n"
            "کیک\n"
            "سکوت\n"
            "اخطار"
        )



    elif text == "قفل‌ها":

        await update.message.reply_text(
            "🔒 قفل‌ها:\n\n"
            "قفل فحش\n"
            "قفل کلمات\n"
            "قفل لینک"
        )



    elif text == "قوانین":

        await update.message.reply_text(
            "📜 قوانین:\n"
            "احترام\n"
            "بدون اسپم"
        )


    elif text == "پشتیبانی":

        await update.message.reply_text(
            "🆘 پشتیبانی iSectorLand"
        )





app = Application.builder().token(TOKEN).build()



app.add_handler(
    CommandHandler(
        "start",
        start
    )
)


app.add_handler(
    CommandHandler(
        "profile",
        profile_cmd
    )
)



# مدیریت

app.add_handler(
    MessageHandler(
        filters.Regex("^بن$"),
        ban
    )
)

app.add_handler(
    MessageHandler(
        filters.Regex("^کیک$"),
        kick
    )
)

app.add_handler(
    MessageHandler(
        filters.Regex("^سکوت$"),
        mute
    )
)

app.add_handler(
    MessageHandler(
        filters.Regex("^اخطار$"),
        warn
    )
)



# قفل‌ها

app.add_handler(
    MessageHandler(
        filters.Regex("^قفل فحش$"),
        lock_bad
    )
)


app.add_handler(
    MessageHandler(
        filters.Regex("^قفل کلمات$"),
        lock_words
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
        filters.Regex("^لیست کلمات$"),
        words_list
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
        filters.Regex("^لیست فحش$"),
        bad_list
    )
)



# اول منو

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        menu_handler
    ),
    group=1
)



# آخر قفل

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        check_locks
    ),
    group=2
)



print("🌻 iSectorLand Started")

app.run_polling()
