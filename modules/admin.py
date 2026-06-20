from telegram import Update
from telegram.ext import ContextTypes
from modules.warnings import add_warn, clear_warn, get_warn


async def is_admin(update, context):
    try:
        admins = await context.bot.get_chat_administrators(update.effective_chat.id)
        return any(a.user.id == update.effective_user.id for a in admins)
    except:
        return False


async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ این دستور فقط برای ادمین‌هاست.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ روی پیام کاربر موردنظر ریپلای کن.")
        return

    user = update.message.reply_to_message.from_user

    # ادمین‌ها رو نمیشه اخطار داد
    admins = await context.bot.get_chat_administrators(update.effective_chat.id)
    if any(a.user.id == user.id for a in admins):
        await update.message.reply_text("⛔️ نمیشه به ادمین اخطار داد.")
        return

    reason = " ".join(context.args) if context.args else "بدون دلیل"
    count = add_warn(user.id)

    if count >= 3:
        await context.bot.ban_chat_member(update.effective_chat.id, user.id)
        clear_warn(user.id)
        await update.message.reply_text(
            f"🚫 <b>{user.first_name}</b> پس از ۳ اخطار بن شد.\n"
            f"🔹 دلیل آخرین اخطار: {reason}",
            parse_mode="HTML"
        )
        return

    await update.message.reply_text(
        f"⚠️ <b>اخطار ثبت شد</b>\n\n"
        f"👤 کاربر: <b>{user.first_name}</b>\n"
        f"📌 دلیل: {reason}\n"
        f"🔢 تعداد اخطار: {count}/3\n\n"
        f"{'⚠️ یک اخطار دیگر و بن میشی!' if count == 2 else ''}",
        parse_mode="HTML"
    )


async def clear_warning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ این دستور فقط برای ادمین‌هاست.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ روی پیام کاربر موردنظر ریپلای کن.")
        return

    user = update.message.reply_to_message.from_user
    clear_warn(user.id)

    await update.message.reply_text(
        f"🧹 تمام اخطارهای <b>{user.first_name}</b> پاک شد.",
        parse_mode="HTML"
    )


async def warns(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ این دستور فقط برای ادمین‌هاست.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ روی پیام کاربر موردنظر ریپلای کن.")
        return

    user = update.message.reply_to_message.from_user
    count = get_warn(user.id)

    await update.message.reply_text(
        f"📋 اخطارهای <b>{user.first_name}</b>: {count}/3",
        parse_mode="HTML"
    )


async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ این دستور فقط برای ادمین‌هاست.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ روی پیام کاربر موردنظر ریپلای کن.")
        return

    user = update.message.reply_to_message.from_user
    admins = await context.bot.get_chat_administrators(update.effective_chat.id)
    if any(a.user.id == user.id for a in admins):
        await update.message.reply_text("⛔️ نمیشه ادمین رو بن کرد.")
        return

    reason = " ".join(context.args) if context.args else "بدون دلیل"

    await context.bot.ban_chat_member(update.effective_chat.id, user.id)
    await update.message.reply_text(
        f"🚫 <b>{user.first_name}</b> بن شد.\n"
        f"🔹 دلیل: {reason}",
        parse_mode="HTML"
    )


async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ این دستور فقط برای ادمین‌هاست.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ روی پیام کاربر موردنظر ریپلای کن.")
        return

    user = update.message.reply_to_message.from_user
    await context.bot.unban_chat_member(update.effective_chat.id, user.id)
    await update.message.reply_text(
        f"✅ <b>{user.first_name}</b> آنبن شد.",
        parse_mode="HTML"
    )


async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ این دستور فقط برای ادمین‌هاست.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ روی پیام کاربر موردنظر ریپلای کن.")
        return

    user = update.message.reply_to_message.from_user
    admins = await context.bot.get_chat_administrators(update.effective_chat.id)
    if any(a.user.id == user.id for a in admins):
        await update.message.reply_text("⛔️ نمیشه ادمین رو کیک کرد.")
        return

    reason = " ".join(context.args) if context.args else "بدون دلیل"

    await context.bot.ban_chat_member(update.effective_chat.id, user.id)
    await context.bot.unban_chat_member(update.effective_chat.id, user.id)
    await update.message.reply_text(
        f"👢 <b>{user.first_name}</b> کیک شد.\n"
        f"🔹 دلیل: {reason}",
        parse_mode="HTML"
    )


async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ این دستور فقط برای ادمین‌هاست.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ روی پیام کاربر موردنظر ریپلای کن.")
        return

    user = update.message.reply_to_message.from_user
    admins = await context.bot.get_chat_administrators(update.effective_chat.id)
    if any(a.user.id == user.id for a in admins):
        await update.message.reply_text("⛔️ نمیشه ادمین رو میوت کرد.")
        return

    from telegram import ChatPermissions
    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        user.id,
        permissions=ChatPermissions(can_send_messages=False)
    )
    await update.message.reply_text(
        f"🔇 <b>{user.first_name}</b> سکوت شد.",
        parse_mode="HTML"
    )


async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ این دستور فقط برای ادمین‌هاست.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ روی پیام کاربر موردنظر ریپلای کن.")
        return

    user = update.message.reply_to_message.from_user

    from telegram import ChatPermissions
    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        user.id,
        permissions=ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
    )
    await update.message.reply_text(
        f"🔊 <b>{user.first_name}</b> آنمیوت شد.",
        parse_mode="HTML"
    )
