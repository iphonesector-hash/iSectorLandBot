import time
from telegram import Update
from telegram.ext import ContextTypes

from modules.settings import get


spam = {}


async def security(update: Update, context):

    if not update.message:
        return


    chat = update.effective_chat.id
    user = update.effective_user.id

    text = update.message.text or ""

    cfg = get(chat)


    # لینک
    if cfg["link"]:

        if "http" in text or "t.me/" in text:

            await update.message.delete()

            await update.message.reply_text(
                "🚫 ارسال لینک ممنوع است"
            )

            return



    # منشن زیاد

    if cfg["mention"]:

        if text.count("@") >= 3:

            await update.message.delete()

            await update.message.reply_text(
                "🚫 منشن زیاد ممنوع"
            )

            return



    # ضد اسپم

    if cfg["spam"]:

        now = time.time()

        old = spam.get(user,0)


        if now-old < 2:

            await update.message.delete()

            return


        spam[user]=now
