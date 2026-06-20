from telegram import Update
from telegram.ext import ContextTypes

from modules.warnings import (
    add_warn,
    clear_warn,
    get_warn
)



async def is_admin(update):

    user = update.effective_user
    chat = update.effective_chat


    admins = await chat.get_administrators()


    for admin in admins:

        if admin.user.id == user.id:
            return True


    return False



async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update):
        await update.message.reply_text(
            "⛔ فقط ادمین‌ها"
        )
        return


    if not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ روی پیام ریپلای کن"
        )
        return


    user = update.message.reply_to_message.from_user

    count = add_warn(user.id)


    await update.message.reply_text(
        f"⚠️ اخطار ثبت شد\n"
        f"تعداد: {count}/3"
    )



async def clear_warn(update, context):

    if not await is_admin(update):
        return


    if not update.message.reply_to_message:
        return


    user = update.message.reply_to_message.from_user

    clear_warn(user.id)


    await update.message.reply_text(
        "🧹 اخطارها پاک شد"
    )



async def ban(update, context):

    if not await is_admin(update):
        return


    if not update.message.reply_to_message:
        return


    user = update.message.reply_to_message.from_user


    await update.message.chat.ban_member(
        user.id
    )


    await update.message.reply_text(
        "🚫 بن شد"
    )



async def kick(update, context):

    if not await is_admin(update):
        return


    if not update.message.reply_to_message:
        return


    user = update.message.reply_to_message.from_user


    await update.message.chat.ban_member(
        user.id
    )


    await update.message.chat.unban_member(
        user.id
    )


    await update.message.reply_text(
        "👢 کیک شد"
    )



async def mute(update, context):

    if not await is_admin(update):
        return


    if not update.message.reply_to_message:
        return


    user = update.message.reply_to_message.from_user


    await update.message.chat.restrict_member(
        user.id,
        permissions={}
    )


    await update.message.reply_text(
        "🔇 سکوت شد"
    )
