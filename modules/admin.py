from telegram import Update
from telegram.ext import ContextTypes


warnings = {}


async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ روی پیام کاربر ریپلای کن"
        )
        return

    user = update.message.reply_to_message.from_user.id

    warnings[user] = warnings.get(user, 0) + 1

    await update.message.reply_text(
        f"⚠️ اخطار داده شد\n"
        f"تعداد اخطار: {warnings[user]}"
    )


async def clear_warn(update: Update, context):

    if not update.message.reply_to_message:
        return

    user = update.message.reply_to_message.from_user.id

    warnings[user] = 0

    await update.message.reply_text(
        "✅ اخطارها پاک شد"
    )


async def ban(update: Update, context):

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "روی پیام کاربر ریپلای کن"
        )
        return

    user = update.message.reply_to_message.from_user.id

    await update.effective_chat.ban_member(user)

    await update.message.reply_text(
        "🚫 کاربر بن شد"
    )


async def kick(update: Update, context):

    if not update.message.reply_to_message:
        return

    user = update.message.reply_to_message.from_user.id

    await update.effective_chat.ban_member(user)

    await update.effective_chat.unban_member(user)

    await update.message.reply_text(
        "👢 کاربر حذف شد"
    )


async def mute(update: Update, context):

    if not update.message.reply_to_message:
        return

    user = update.message.reply_to_message.from_user.id

    await update.effective_chat.restrict_member(
        user,
        permissions={}
    )

    await update.message.reply_text(
        "🔇 کاربر ساکت شد"
    )
