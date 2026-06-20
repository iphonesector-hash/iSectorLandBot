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
from modules.settings import *
from modules.profile import *

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

    for x in [
        "🎮","🛠","🛡","🔒",
        "👤","📜","⚙️","🆘",
        "😂","🧠","🎲","🪙"
    ]:
        text = text.replace(x,"")

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



async def profile_cmd(update,context):

    await profile(update,context)



# ---------- قفل‌ها ----------

async def lock_commands(update, context):

    text = update.message.text


    if text == "قفل لینک":
        await lock_link(update,context)

    elif text == "حذف قفل لینک":
        await unlock_link(update,context)

    elif text == "قفل فوروارد":
        await lock_forward(update,context)

    elif text == "حذف قفل فوروارد":
        await unlock_forward(update,context)

    elif text == "قفل یوزرنیم":
        await lock_username(update,context)

    elif text == "حذف قفل یوزرنیم":
        await unlock_username(update,context)

    elif text == "قفل عکس":
        await lock_photo(update,context)

    elif text == "حذف قفل عکس":
        await unlock_photo(update,context)

    elif text == "قفل ویدیو":
        await lock_video(update,context)

    elif text == "حذف قفل ویدیو":
        await unlock_video(update,context)

    elif text == "قفل فایل":
        await lock_file(update,context)

    elif text == "حذف قفل فایل":
        await unlock_file(update,context)

    elif text == "قفل استیکر":
        await lock_sticker(update,context)

    elif text == "حذف قفل استیکر":
        await unlock_sticker(update,context)





async def menu_handler(update,context):

    text = clean(update.message.text)



    if text == "سرگرمی":

        await update.message.reply_text(
            "🎮 سرگرمی:\n\n"
            "😂 جوک\n"
            "🧠 چیستان\n"
            "🎲 تاس\n"
            "🪙 شیر یا خط"
        )


    elif text == "جوک":
        await update.message.reply_text(get_joke())


    elif text == "چیستان":
        await update.message.reply_text(riddle())


    elif text == "تاس":
        await update.message.reply_text(dice())


    elif text == "شیر یا خط":
        await update.message.reply_text(coin())


    elif text == "پروفایل":
        await profile_cmd(update,context)


    elif text == "مدیریت":

        await update.message.reply_text(
            "🛡 مدیریت:\n\n"
            "اخطار\n"
            "پاک کردن اخطار\n"
            "بن\n"
            "کیک\n"
            "سکوت"
        )


    elif text == "قفل‌ها":

        await update.message.reply_text(
            "🔒 قفل‌ها:\n\n"
            "قفل لینک\n"
            "حذف قفل لینک\n"
            "قفل فوروارد\n"
            "حذف قفل فوروارد\n"
            "قفل یوزرنیم\n"
            "حذف قفل یوزرنیم\n"
            "قفل عکس\n"
            "حذف قفل عکس\n"
            "قفل ویدیو\n"
            "حذف قفل ویدیو\n"
            "قفل فایل\n"
            "حذف قفل فایل\n"
            "قفل استیکر\n"
            "حذف قفل استیکر"
        )



app = Application.builder().token(TOKEN).build()



app.add_handler(
    CommandHandler("start",start)
)

app.add_handler(
    CommandHandler("profile",profile_cmd)
)



# قفل‌ها بالاتر از همه

app.add_handler(
    MessageHandler(
        filters.Regex(
        "^(قفل لینک|حذف قفل لینک|قفل فوروارد|حذف قفل فوروارد|قفل یوزرنیم|حذف قفل یوزرنیم|قفل عکس|حذف قفل عکس|قفل ویدیو|حذف قفل ویدیو|قفل فایل|حذف قفل فایل|قفل استیکر|حذف قفل استیکر)$"
        ),
        lock_commands
    ),
    group=0
)



# مدیریت

app.add_handler(MessageHandler(filters.Regex("^اخطار$"),warn))
app.add_handler(MessageHandler(filters.Regex("^(پاک کردن اخطار|حذف اخطار)$"),clear_warn))
app.add_handler(MessageHandler(filters.Regex("^بن$"),ban))
app.add_handler(MessageHandler(filters.Regex("^کیک$"),kick))
app.add_handler(MessageHandler(filters.Regex("^سکوت$"),mute))



# قفل محتوا

app.add_handler(
    MessageHandler(
        filters.ALL & ~filters.COMMAND,
        check_locks
    ),
    group=1
)



# منو آخر

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        menu_handler
    ),
    group=2
)



print("🌻 iSectorLand Started")

app.run_polling()
