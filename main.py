from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)

from modules.fun import *
from modules.admin import (
    warn,
    clear_warning,
    ban,
    kick,
    mute
)

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



def clean(text):

    if not text:
        return ""

    emojis = [
        "🎮","🛠","🛡","🔒",
        "👤","📜","⚙️","🆘"
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

    user = get_user(
        update.effective_user
    )

    await update.message.reply_text(
        f"👤 پروفایل\n\n"
        f"نام: {user['name']}\n"
        f"⭐ لول: {user['level']}\n"
        f"🪙 سکه: {user['coins']}\n"
        f"💎 VIP: {user['vip']}"
    )





async def lock_handler(update, context):

    text = update.message.text.strip()


    cmds = {

        "قفل لینک": lock_link,
        "حذف قفل لینک": unlock_link,

        "قفل فوروارد": lock_forward,
        "حذف قفل فوروارد": unlock_forward,

        "قفل یوزرنیم": lock_username,
        "حذف قفل یوزرنیم": unlock_username,

        "قفل عکس": lock_photo,
        "حذف قفل عکس": unlock_photo,

        "قفل ویدیو": lock_video,
        "حذف قفل ویدیو": unlock_video,

        "قفل فایل": lock_file,
        "حذف قفل فایل": unlock_file,

        "قفل استیکر": lock_sticker,
        "حذف قفل استیکر": unlock_sticker
    }


    if text in cmds:
        await cmds[text](update, context)







async def menu_handler(update, context):

    text = clean(
        update.message.text
    )



    if text == "سرگرمی":

        await update.message.reply_text(
            "🎮 سرگرمی:\n\n"
            "😂 جوک\n"
            "📚 فکت\n"
            "💪 انگیزشی\n"
            "✨ متن\n"
            "🎲 تاس\n"
            "🪙 شیر یا خط\n"
            "🧠 چیستان"
        )



    elif text == "جوک":
        await update.message.reply_text(
            get_joke()
        )


    elif text == "فکت":
        await update.message.reply_text(
            get_fact()
        )


    elif text == "انگیزشی":
        await update.message.reply_text(
            get_motive()
        )


    elif text == "متن":
        await update.message.reply_text(
            get_text()
        )


    elif text == "تاس":
        await update.message.reply_text(
            dice()
        )


    elif text == "شیر یا خط":
        await update.message.reply_text(
            coin()
        )


    elif text == "چیستان":
        await update.message.reply_text(
            riddle()
        )




    elif text == "مدیریت":

        await update.message.reply_text(
            "🛡 مدیریت:\n\n"
            "دستورات:\n\n"
            "/warn\n"
            "/clearwarn\n"
            "/ban\n"
            "/kick\n"
            "/mute"
        )




    elif text == "قوانین":

        await update.message.reply_text(
            "📜 قوانین:\n\n"
            "• اسپم ممنوع\n"
            "• تبلیغات ممنوع\n"
            "• بی احترامی ممنوع"
        )




    elif text == "کاربردی":

        await update.message.reply_text(
            "🛠 کاربردی:\n\n"
            "بخش کاربردی فعال شد"
        )




    elif text == "تنظیمات":

        await update.message.reply_text(
            "⚙️ تنظیمات:\n\n"
            "تنظیمات گروه از طریق ادمین انجام می‌شود"
        )




    elif text == "پشتیبانی":

        await update.message.reply_text(
            "🆘 پشتیبانی:\n\n"
            "برای کمک پیام ارسال کنید"
        )




    elif text == "قفل‌ها":

        await update.message.reply_text(
            "🔒 قفل‌ها:\n\n"

            "قفل لینک\n"
            "حذف قفل لینک\n\n"

            "قفل فوروارد\n"
            "حذف قفل فوروارد\n\n"

            "قفل یوزرنیم\n"
            "حذف قفل یوزرنیم\n\n"

            "قفل عکس\n"
            "حذف قفل عکس\n\n"

            "قفل ویدیو\n"
            "حذف قفل ویدیو\n\n"

            "قفل فایل\n"
            "حذف قفل فایل\n\n"

            "قفل استیکر\n"
            "حذف قفل استیکر"
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
    CommandHandler("warn", warn)
)

app.add_handler(
    CommandHandler("clearwarn", clear_warning)
)

app.add_handler(
    CommandHandler("ban", ban)
)

app.add_handler(
    CommandHandler("kick", kick)
)

app.add_handler(
    CommandHandler("mute", mute)
)





# قفل‌ها اول

app.add_handler(
    MessageHandler(
        filters.Regex(
            "^(قفل لینک|حذف قفل لینک|قفل فوروارد|حذف قفل فوروارد|قفل یوزرنیم|حذف قفل یوزرنیم|قفل عکس|حذف قفل عکس|قفل ویدیو|حذف قفل ویدیو|قفل فایل|حذف قفل فایل|قفل استیکر|حذف قفل استیکر)$"
        ),
        lock_handler
    ),
    group=0
)





# منو

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        menu_handler
    ),
    group=1
)





# بررسی قفل محتوا آخر

app.add_handler(
    MessageHandler(
        filters.ALL & ~filters.COMMAND,
        check_locks
    ),
    group=10
)





print("🌻 iSectorLand Started")


app.run_polling()
