from telegram import Update
from telegram.ext import ContextTypes


async def is_admin(update, context):

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id


    admins = await context.bot.get_chat_administrators(chat_id)


    for admin in admins:

        if admin.user.id == user_id:
            return True


    return False



async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update, context):
        await update.message.reply_text("⛔ فقط ادمین‌ها")
        return


    if not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ روی پیام کاربر ریپلای کن"
        )
        return


    user = update.message.reply_to_message.from_user


    await update.message.reply_text(
        f"⚠️ اخطار برای {user.first_name} ثبت شد"
    )



async def clear_warn(update, context):

    if not await is_admin(update, context):
        return


    await update.message.reply_text(
        "🧹 اخطار پاک شد"
    )



async def ban(update, context):

    if not await is_admin(update, context):
        await update.message.reply_text("⛔ فقط ادمین‌ها")
        return


    if not update.message.reply_to_message:
        await update.message.reply_text(
            "🚫 روی پیام کاربر ریپلای کن"
        )
        return


    user = update.message.reply_to_message.from_user


    await context.bot.ban_chat_member(
        update.effective_chat.id,
        user.id
    )


    await update.message.reply_text(
        "🚫 کاربر بن شد"
    )



async def kick(update, context):

    if not await is_admin(update, context):
        return


    if not update.message.reply_to_message:
        return


    user = update.message.reply_to_message.from_user


    await context.bot.ban_chat_member(
        update.effective_chat.id,
        user.id
    )

    await context.bot.unban_chat_member(
        update.effective_chat.id,
        user.id
    )


    await update.message.reply_text(
        "👢 کاربر کیک شد"
    )



async def mute(update, context):

    if not await is_admin(update, context):
        return


    if not update.message.reply_to_message:
        return


    user = update.message.reply_to_message.from_user


    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        user.id,
        permissions={
            "can_send_messages": False
        }
    )


    await update.message.reply_text(
        "🔇 کاربر سکوت شد"
    )
