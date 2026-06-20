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

    for e in [
        "🎮","🛠","🛡","🔒",
        "👤","📜","⚙️","🆘"
    ]:
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



# تست و دستورات قفل

async def lock_handler(update, context):

    text = update.message.text.strip()

    if text == "قفل لینک":
        await lock_link(update, context)

    elif text == "حذف قفل لینک":
        await unlock_link(update, context)

    elif text == "قفل فوروارد":
        await lock_forward(update, context)

    elif text == "حذف قفل فوروارد":
        await unlock_forward(update, context)

    elif text == "قفل یوزرنیم":
        await lock_username(update, context)

    elif text == "حذف قفل یوزرنیم":
        await unlock_username(update, context)

    elif text == "قفل عکس":
        await lock_photo(update, context)

    elif text == "حذف قفل عکس":
        await unlock_photo(update, context)

    elif text == "قفل ویدیو":
        await lock_video(update, context)

    elif text == "حذف قفل ویدیو":
        await unlock_video(update, context)

    elif text == "قفل فایل":
        await lock_file(update, context)

    elif text == "حذف قفل فایل":
        await unlock_file(update, context)

    elif text == "قفل استیکر":
        await lock_sticker(update, context)

    elif text == "حذف قفل استیکر":
        await unlock_sticker(update, context)





async def menu_handler(update, context):

    text = clean(update.message.text)


    if text == "سرگرمی":

        await update.message.reply_text(
            "🎮 سرگرمی:\n\n"
            "😂 جوک\n"
            "🧠 چیستان\n"
            "🎲 تاس"
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


    elif text == "پروفایل":

        await profile_cmd(update, context)



    elif text == "قفل‌ها":

        await update.message.reply_text(
            "🔒 قفل‌ها:\n\n"
            "قفل لینک\n"
            "حذف قفل لینک\n"
            "قفل فوروارد\n"
            "حذف قفل فوروارد\n"
            "قفل یوزرنیم\n"
            "حذف قفل یوزرنیم"
        )





app = Application.builder().token(TOKEN).build()



app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CommandHandler("profile", profile_cmd)
)



# اول قفل‌ها

app.add_handler(
    MessageHandler(
        filters.Regex(
            "^(قفل لینک|حذف قفل لینک|قفل فوروارد|حذف قفل فوروارد|قفل یوزرنیم|حذف قفل یوزرنیم|قفل عکس|حذف قفل عکس|قفل ویدیو|حذف قفل ویدیو|قفل فایل|حذف قفل فایل|قفل استیکر|حذف قفل استیکر)$"
        ),
        lock_handler
    ),
    group=0
)



# تست اینکه پیام می‌رسه

async def test_message(update, context):

    if update.message.text == "تست":

        await update.message.reply_text(
            "ربات پیام گرفت"
        )


app.add_handler(
    MessageHandler(
        filters.TEXT,
        test_message
    ),
    group=1
)



# قفل محتوا

app.add_handler(
    MessageHandler(
        filters.ALL & ~filters.COMMAND,
        check_locks
    ),
    group=2
)



# منو آخر

app.add_handler(
    MessageHandler(
        filters.TEXT,
        menu_handler
    ),
    group=3
)



print("🌻 iSectorLand Started")

app.run_polling()
