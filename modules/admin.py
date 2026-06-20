from telegram import Update
from telegram.ext import ContextTypes

from modules.warnings import (
    add_warn,
    clear_warn,
    get_warn
)


OWNER_ID = 5147526780


async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ روی پیام کاربر ریپلای کن"
        )
        return


    user = update.message.reply_to_message.from_user

    count = add_warn(user.id)


    await update.message.reply_text(
        f"⚠️ اخطار ثبت شد\n\n"
        f"👤 {user.first_name}\n"
        f"تعداد اخطار: {count}/3"
    )


    if count >= 3:

        await update.message.chat.ban_member(
            user.id
        )

        await update.message.reply_text(
            "🚫 کاربر به دلیل رسیدن به ۳ اخطار بن شد"
        )



async def clear_warn(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        return


    user = update.message.reply_to_message.from_user

    clear_warn(user.id)


    await update.message.reply_text(
        "🧹 اخطارهای کاربر پاک شد"
    )



async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "🚫 روی پیام کاربر ریپلای کن"
        )
        return


    user = update.message.reply_to_message.from_user

    await update.message.chat.ban_member(
        user.id
    )

    await update.message.reply_text(
        "🚫 کاربر بن شد"
    )



async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):

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



async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        return


    user = update.message.reply_to_message.from_user


    await update.message.chat.restrict_member(
        user.id,
        permissions={}
    )


    await update.message.reply_text(
        "🔇 کاربر سکوت شد"
    )
