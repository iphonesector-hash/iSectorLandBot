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

    for e in [
        "🎮","🛠","🛡","🔒",
        "👤","📜","⚙️","🆘",
        "😂","🧠","🎲","🪙"
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



async def menu_handler(update, context):

    if not update.message:
        return

    text = clean_text(update.message.text)



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
        await profile_cmd(update, context)


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


    elif text == "قوانین":

        await update.message.reply_text(
            "📜 قوانین فعال است"
        )


    elif text == "پشتیبانی":

        await update.message.reply_text(
            "🆘 پشتیبانی iSectorLand"
        )





app = Application.builder().token(TOKEN).build()



app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("profile", profile_cmd))



# مدیریت

app.add_handler(MessageHandler(filters.Regex("^اخطار$"), warn))

app.add_handler(
    MessageHandler(
        filters.Regex("^(پاک کردن اخطار|حذف اخطار)$"),
        clear_warning
    )
)

app.add_handler(MessageHandler(filters.Regex("^بن$"), ban))
app.add_handler(MessageHandler(filters.Regex("^کیک$"), kick))
app.add_handler(MessageHandler(filters.Regex("^سکوت$"), mute))



# قفل‌ها

app.add_handler(MessageHandler(filters.Regex("^قفل لینک$"), lock_link))
app.add_handler(MessageHandler(filters.Regex("^حذف قفل لینک$"), unlock_link))

app.add_handler(MessageHandler(filters.Regex("^قفل فوروارد$"), lock_forward))
app.add_handler(MessageHandler(filters.Regex("^حذف قفل فوروارد$"), unlock_forward))

app.add_handler(MessageHandler(filters.Regex("^قفل یوزرنیم$"), lock_username))
app.add_handler(MessageHandler(filters.Regex("^حذف قفل یوزرنیم$"), unlock_username))

app.add_handler(MessageHandler(filters.Regex("^قفل عکس$"), lock_photo))
app.add_handler(MessageHandler(filters.Regex("^حذف قفل عکس$"), unlock_photo))

app.add_handler(MessageHandler(filters.Regex("^قفل ویدیو$"), lock_video))
app.add_handler(MessageHandler(filters.Regex("^حذف قفل ویدیو$"), unlock_video))

app.add_handler(MessageHandler(filters.Regex("^قفل فایل$"), lock_file))
app.add_handler(MessageHandler(filters.Regex("^حذف قفل فایل$"), unlock_file))

app.add_handler(MessageHandler(filters.Regex("^قفل استیکر$"), lock_sticker))
app.add_handler(MessageHandler(filters.Regex("^حذف قفل استیکر$"), unlock_sticker))



# منو

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        menu_handler
    ),
    group=0
)



# چک قفل‌ها

app.add_handler(
    MessageHandler(
        filters.ALL & ~filters.COMMAND,
        check_locks
    ),
    group=1
)



print("🌻 iSectorLand Started")

app.run_polling()
