from telegram import Update
from telegram.ext import ContextTypes


bad_words = [
    "فحش۱",
    "فحش۲"
]

blocked_words = [
    "کلمه۱",
    "کلمه۲"
]


settings = {
    "bad_lock": True,
    "word_lock": True
}


async def check_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    text = update.message.text.lower()


    if settings["bad_lock"]:

        for word in bad_words:

            if word in text:

                await update.message.delete()

                await update.message.reply_text(
                    "🚫 پیام به دلیل فحش حذف شد"
                )

                return



    if settings["word_lock"]:

        for word in blocked_words:

            if word in text:

                await update.message.delete()

                await update.message.reply_text(
                    "🚫 این کلمه مجاز نیست"
                )

                return



async def lock_bad(update, context):

    settings["bad_lock"] = True

    await update.message.reply_text(
        "🔒 قفل فحش فعال شد"
    )


async def unlock_bad(update, context):

    settings["bad_lock"] = False

    await update.message.reply_text(
        "🔓 قفل فحش خاموش شد"
    )


async def lock_words(update, context):

    settings["word_lock"] = True

    await update.message.reply_text(
        "🔒 قفل کلمات فعال شد"
    )


async def unlock_words(update, context):

    settings["word_lock"] = False

    await update.message.reply_text(
        "🔓 قفل کلمات خاموش شد"
    )
