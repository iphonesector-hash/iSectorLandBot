from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes

from modules.warnings import (
    add_warn,
    remove_warn,
    get_warn
)


OWNER_ID = 5147526780


def is_admin(update):
    return update.effective_user.id == OWNER_ID



async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update):
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ روی پیام کاربر ریپلای کن"
        )
        return


    user = update.message.reply_to_message.from_user
    chat = update.effective_chat


    count = add_warn(
        chat.id,
        user.id
    )


    await update.message.reply_text(
        f"⚠️ اخطار ثبت شد\n\n"
        f"👤 {user.first_name}\n"
        f"🔢 تعداد: {count}/3"
    )


    if count >= 3:

        try:
            await chat.ban_member(user.id)

            await update.message.reply_text(
                "🚫 کاربر با ۳ اخطار بن شد"
            )

        except:
            await update.message.reply_text(
                "❌ دسترسی بن ندارم"
            )



async def clear_warn(update: Update, context):

    if not is_admin(update):
        return


    if not update.message.reply_to_message:
        await update.message.reply_text(
            "🧹 روی پیام کاربر ریپلای کن"
        )
        return


    user = update.message.reply_to_message.from_user


    remove_warn(
        update.effective_chat.id,
        user.id
    )


    await update.message.reply_text(
        "🧹 اخطارهای کاربر پاک شد"
    )



async def ban(update: Update, context):

    if not is_admin(update):
        return


    if not update.message.reply_to_message:
        return


    user = update.message.reply_to_message.from_user


    await update.message.chat.ban_member(
        user.id
    )


    await update.message.reply_text(
        "🚫 کاربر بن شد"
    )



async def kick(update: Update, context):

    if not is_admin(update):
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
        "👢 کاربر کیک شد"
    )



async def mute(update: Update, context):

    if not is_admin(update):
        return


    if not update.message.reply_to_message:
        return


    user = update.message.reply_to_message.from_user


    await update.message.chat.restrict_member(
        user.id,
        permissions=ChatPermissions(
            can_send_messages=False
        )
    )


    await update.message.reply_text(
        "🔇 کاربر سکوت شد"
    )



async def unmute(update: Update, context):

    if not is_admin(update):
        return


    if not update.message.reply_to_message:
        return


    user = update.message.reply_to_message.from_user


    await update.message.chat.restrict_member(
        user.id,
        permissions=ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
    )


    await update.message.reply_text(
        "🔊 سکوت کاربر برداشته شد"
    )
