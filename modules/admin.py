import json
import os
from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from modules.warnings import add_warn, clear_warn, get_warn

# ─── تنظیمات اخطار ─────────────────────────────────────
WARN_SETTINGS_FILE = "warn_settings.json"

def load_warn_settings():
    if not os.path.exists(WARN_SETTINGS_FILE):
        return {}
    with open(WARN_SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_warn_settings(data):
    with open(WARN_SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_warn_limit(chat_id):
    data = load_warn_settings()
    return data.get(str(chat_id), {}).get("limit", 3)

def set_warn_limit(chat_id, limit):
    data = load_warn_settings()
    cid = str(chat_id)
    if cid not in data:
        data[cid] = {}
    data[cid]["limit"] = limit
    save_warn_settings(data)


# ─── چک ادمین ──────────────────────────────────────────
async def is_admin(update, context):
    try:
        admins = await context.bot.get_chat_administrators(update.effective_chat.id)
        return any(a.user.id == update.effective_user.id for a in admins)
    except:
        return False


# ─── دستور: اخطار ──────────────────────────────────────
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ فقط ادمین‌ها میتونن اخطار بدن.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ روی پیام کاربر موردنظر ریپلای کن.")
        return

    user = update.message.reply_to_message.from_user

    admins = await context.bot.get_chat_administrators(update.effective_chat.id)
    if any(a.user.id == user.id for a in admins):
        await update.message.reply_text("⛔️ نمیشه به ادمین اخطار داد.")
        return

    reason = " ".join(context.args) if context.args else "بدون دلیل"
    count = add_warn(user.id)
    limit = get_warn_limit(update.effective_chat.id)

    if count >= limit:
        await context.bot.ban_chat_member(update.effective_chat.id, user.id)
        clear_warn(user.id)
        await update.message.reply_text(
            f"🚫 <b>{user.first_name}</b> پس از {limit} اخطار بن شد.\n"
            f"🔹 دلیل: {reason}",
            parse_mode="HTML"
        )
        return

    bar = "🔴" * count + "⚪️" * (limit - count)

    await update.message.reply_text(
        f"⚠️ <b>اخطار ثبت شد</b>\n\n"
        f"👤 کاربر: <b>{user.first_name}</b>\n"
        f"📌 دلیل: {reason}\n"
        f"🔢 اخطار: {bar} ({count}/{limit})\n\n"
        f"{'🚨 یک اخطار دیگر و بن میشی!' if count == limit - 1 else ''}",
        parse_mode="HTML"
    )


# ─── دستور: پاک کردن اخطار ─────────────────────────────
async def clear_warning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ فقط ادمین‌ها میتونن اخطار پاک کنن.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ روی پیام کاربر موردنظر ریپلای کن.")
        return

    user = update.message.reply_to_message.from_user
    clear_warn(user.id)

    await update.message.reply_text(
        f"🧹 اخطارهای <b>{user.first_name}</b> پاک شد.",
        parse_mode="HTML"
    )


# ─── دستور: مشاهده اخطار ───────────────────────────────
async def warns(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ فقط ادمین‌ها.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ روی پیام کاربر موردنظر ریپلای کن.")
        return

    user = update.message.reply_to_message.from_user
    count = get_warn(user.id)
    limit = get_warn_limit(update.effective_chat.id)
    bar = "🔴" * count + "⚪️" * (limit - count)

    await update.message.reply_text(
        f"📋 اخطارهای <b>{user.first_name}</b>:\n{bar} ({count}/{limit})",
        parse_mode="HTML"
    )


# ─── دستور: تنظیم حد اخطار ─────────────────────────────
async def setwarnlimit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ فقط ادمین‌ها.")
        return

    if not context.args or not context.args[0].isdigit():
        limit = get_warn_limit(update.effective_chat.id)
        await update.message.reply_text(
            f"⚙️ حد اخطار فعلی: <b>{limit}</b>\n\n"
            f"برای تغییر بنویس:\n<code>اخطار حد [عدد]</code>\n"
            f"مثال: <code>اخطار حد 5</code>",
            parse_mode="HTML"
        )
        return

    limit = int(context.args[0])
    if limit < 1 or limit > 10:
        await update.message.reply_text("❌ عدد باید بین ۱ تا ۱۰ باشه.")
        return

    set_warn_limit(update.effective_chat.id, limit)
    await update.message.reply_text(
        f"✅ حد اخطار به <b>{limit}</b> تغییر کرد.",
        parse_mode="HTML"
    )


# ─── دستور: بن ─────────────────────────────────────────
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ فقط ادمین‌ها میتونن بن کنن.")
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
        f"🚫 <b>{user.first_name}</b> بن شد.\n🔹 دلیل: {reason}",
        parse_mode="HTML"
    )


# ─── دستور: آنبن ───────────────────────────────────────
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ فقط ادمین‌ها میتونن آنبن کنن.")
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


# ─── دستور: کیک ────────────────────────────────────────
async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ فقط ادمین‌ها میتونن کیک کنن.")
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
        f"👢 <b>{user.first_name}</b> کیک شد.\n🔹 دلیل: {reason}",
        parse_mode="HTML"
    )


# ─── دستور: میوت ───────────────────────────────────────
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ فقط ادمین‌ها میتونن میوت کنن.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ روی پیام کاربر موردنظر ریپلای کن.")
        return

    user = update.message.reply_to_message.from_user
    admins = await context.bot.get_chat_administrators(update.effective_chat.id)
    if any(a.user.id == user.id for a in admins):
        await update.message.reply_text("⛔️ نمیشه ادمین رو میوت کرد.")
        return

    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        user.id,
        permissions=ChatPermissions(can_send_messages=False)
    )
    await update.message.reply_text(
        f"🔇 <b>{user.first_name}</b> سکوت شد.",
        parse_mode="HTML"
    )


# ─── دستور: آنمیوت ─────────────────────────────────────
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ فقط ادمین‌ها میتونن آنمیوت کنن.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ روی پیام کاربر موردنظر ریپلای کن.")
        return

    user = update.message.reply_to_message.from_user
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


# ─── هندلر متنی فارسی برای دستورات مدیریت ─────────────
async def admin_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """این هندلر پیام‌های فارسی مدیریتی رو پردازش میکنه"""
    text = update.message.text.strip()

    # تنظیم حد اخطار: "اخطار حد 5"
    if text.startswith("اخطار حد"):
        parts = text.split()
        if len(parts) == 3 and parts[2].isdigit():
            context.args = [parts[2]]
        else:
            context.args = []
        await setwarnlimit(update, context)
        return

    cmd_map = {
        "اخطار": warn,
        "پاک اخطار": clear_warning,
        "اخطارها": warns,
        "بن": ban,
        "آنبن": unban,
        "کیک": kick,
        "میوت": mute,
        "آنمیوت": unmute,
    }

    if text in cmd_map:
        context.args = []
        await cmd_map[text](update, context)
