from telegram import Update
from telegram.ext import ContextTypes

from modules.warnings import (
    add_warn,
    clear_warn,
    get_warn
)



async def is_admin(update, context):

    admins = await context.bot.get_chat_administrators(
        update.effective_chat.id
    )

    for admin in admins:
        if admin.user.id == update.effective_user.id:
            return True

    return False



async def warn(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await is_admin(update, context):
        await update.message.reply_text(
            "⛔ فقط ادمین‌ها"
        )
        return



    if not update.message.reply_to_message:

        await update.message.reply_text(
            "⚠️ روی پیام کاربر ریپلای کن"
        )

        return



    user = update.message.reply_to_message.from_user


    count = add_warn(
        user.id
    )



    if count >= 3:


        await context.bot.ban_chat_member(
            update.effective_chat.id,
            user.id
        )


        await update.message.reply_text(
            f"🚫 {user.first_name} به دلیل ۳ اخطار بن شد"
        )


        clear_warn(
            user.id
        )

        return



    await update.message.reply_text(
        f"⚠️ اخطار ثبت شد\n\n"
        f"👤 {user.first_name}\n"
        f"تعداد اخطار: {count}/3"
    )





async def clear_warning(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


    if not await is_admin(update, context):
        return



    if not update.message.reply_to_message:
        return



    user = update.message.reply_to_message.from_user


    clear_warn(
        user.id
    )


    await update.message.reply_text(
        "🧹 اخطارهای کاربر پاک شد"
    )





async def ban(
    update,
    context
):

    if not await is_admin(update, context):
        return


    if not update.message.reply_to_message:
        return


    user = update.message.reply_to_message.from_user


    await context.bot.ban_chat_member(
        update.effective_chat.id,
        user.id
    )


    await update.message.reply_text(
        "🚫 کاربر بن شد"
    )





async def kick(
    update,
    context
):

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





async def mute(
    update,
    context
):

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
