import json
import os
from telegram import ChatPermissions
from modules.warnings import add_warn, clear_warn, get_warn

WARN_SETTINGS_FILE = "warn_settings.json"


def load_warn_settings() -> dict:
    if not os.path.exists(WARN_SETTINGS_FILE):
        return {}
    with open(WARN_SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_warn_settings(data: dict):
    with open(WARN_SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_warn_limit(chat_id) -> int:
    data = load_warn_settings()
    return data.get(str(chat_id), {}).get("limit", 3)


def set_warn_limit(chat_id, limit: int):
    data = load_warn_settings()
    cid = str(chat_id)
    if cid not in data:
        data[cid] = {}
    data[cid]["limit"] = limit
    save_warn_settings(data)


async def is_admin(update, context) -> bool:
    try:
        admins = await context.bot.get_chat_administrators(update.effective_chat.id)
        return any(a.user.id == update.effective_user.id for a in admins)
    except Exception:
        return False


async def get_target(update):
    """برمیگردونه کاربر هدف از ریپلای"""
    if update.message.reply_to_message:
        return update.message.reply_to_message.from_user
    return None


# ─── اخطار ─────────────────────────────────────────────
async def warn(update, context):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ فقط ادمین‌ها می‌تونن اخطار بدن.")
        return
    user = await get_target(update)
    if not user:
        await update.message.reply_text("↩️ روی پیام کاربر موردنظر ریپلای کن.")
        return
    admins = await context.bot.get_chat_administrators(update.effective_chat.id)
    if any(a.user.id == user.id for a in admins):
        await update.message.reply_text("⛔️ نمیشه به ادمین اخطار داد.")
        return
    reason = " ".join(context.args) if context.args else "بدون دلیل"
    count = add_warn(user.id)
    limit = get_warn_limit(update.effective_chat.id)
    if count >= limit:
        try:
            await context.bot.ban_chat_member(update.effective_chat.id, user.id)
            clear_warn(user.id)
        except Exception:
            pass
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
        f"🔢 اخطار: {bar} ({count}/{limit})\n"
        f"{'🚨 یک اخطار دیگه و بن میشی!' if count == limit - 1 else ''}",
        parse_mode="HTML"
    )


# ─── پاک کردن اخطار ────────────────────────────────────
async def clear_warning(update, context):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ فقط ادمین‌ها.")
        return
    user = await get_target(update)
    if not user:
        await update.message.reply_text("↩️ روی پیام کاربر موردنظر ریپلای کن.")
        return
    clear_warn(user.id)
    await update.message.reply_text(
        f"🧹 اخطارهای <b>{user.first_name}</b> پاک شد.",
        parse_mode="HTML"
    )


# ─── مشاهده اخطار ──────────────────────────────────────
async def warns(update, context):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ فقط ادمین‌ها.")
        return
    user = await get_target(update)
    if not user:
        await update.message.reply_text("↩️ روی پیام کاربر موردنظر ریپلای کن.")
        return
    count = get_warn(user.id)
    limit = get_warn_limit(update.effective_chat.id)
    bar = "🔴" * count + "⚪️" * (limit - count)
    await update.message.reply_text(
        f"📋 اخطارهای <b>{user.first_name}</b>:\n{bar} ({count}/{limit})",
        parse_mode="HTML"
    )


# ─── تنظیم حد اخطار ────────────────────────────────────
async def setwarnlimit(update, context):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ فقط ادمین‌ها.")
        return
    if not context.args or not context.args[0].isdigit():
        limit = get_warn_limit(update.effective_chat.id)
        await update.message.reply_text(
            f"⚙️ حد اخطار فعلی: <b>{limit}</b>\n"
            f"مثال: <code>/setwarnlimit 5</code>",
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


# ─── بن ────────────────────────────────────────────────
async def ban(update, context):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ فقط ادمین‌ها می‌تونن بن کنن.")
        return
    user = await get_target(update)
    if not user:
        await update.message.reply_text("↩️ روی پیام کاربر موردنظر ریپلای کن.")
        return
    admins = await context.bot.get_chat_administrators(update.effective_chat.id)
    if any(a.user.id == user.id for a in admins):
        await update.message.reply_text("⛔️ نمیشه ادمین رو بن کرد.")
        return
    reason = " ".join(context.args) if context.args else "بدون دلیل"
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, user.id)
        await update.message.reply_text(
            f"🚫 <b>{user.first_name}</b> بن شد.\n🔹 دلیل: {reason}",
            parse_mode="HTML"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ خطا در بن کردن: {e}")


# ─── آن‌بن ──────────────────────────────────────────────
async def unban(update, context):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ فقط ادمین‌ها می‌تونن آن‌بن کنن.")
        return
    user = await get_target(update)
    if not user:
        await update.message.reply_text("↩️ روی پیام کاربر موردنظر ریپلای کن.")
        return
    try:
        await context.bot.unban_chat_member(update.effective_chat.id, user.id)
        await update.message.reply_text(
            f"✅ <b>{user.first_name}</b> آن‌بن شد.",
            parse_mode="HTML"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ خطا: {e}")


# ─── کیک ───────────────────────────────────────────────
async def kick(update, context):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ فقط ادمین‌ها می‌تونن کیک کنن.")
        return
    user = await get_target(update)
    if not user:
        await update.message.reply_text("↩️ روی پیام کاربر موردنظر ریپلای کن.")
        return
    admins = await context.bot.get_chat_administrators(update.effective_chat.id)
    if any(a.user.id == user.id for a in admins):
        await update.message.reply_text("⛔️ نمیشه ادمین رو کیک کرد.")
        return
    reason = " ".join(context.args) if context.args else "بدون دلیل"
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, user.id)
        await context.bot.unban_chat_member(update.effective_chat.id, user.id)
        await update.message.reply_text(
            f"👢 <b>{user.first_name}</b> اخراج شد.\n🔹 دلیل: {reason}",
            parse_mode="HTML"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ خطا: {e}")


# ─── سکوت ──────────────────────────────────────────────
async def mute(update, context):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ فقط ادمین‌ها می‌تونن سکوت بدن.")
        return
    user = await get_target(update)
    if not user:
        await update.message.reply_text("↩️ روی پیام کاربر موردنظر ریپلای کن.")
        return
    admins = await context.bot.get_chat_administrators(update.effective_chat.id)
    if any(a.user.id == user.id for a in admins):
        await update.message.reply_text("⛔️ نمیشه ادمین رو سکوت کرد.")
        return
    try:
        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            user.id,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await update.message.reply_text(
            f"🔇 <b>{user.first_name}</b> سکوت شد.",
            parse_mode="HTML"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ خطا: {e}")


# ─── رفع سکوت ──────────────────────────────────────────
async def unmute(update, context):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔️ فقط ادمین‌ها می‌تونن رفع سکوت کنن.")
        return
    user = await get_target(update)
    if not user:
        await update.message.reply_text("↩️ روی پیام کاربر موردنظر ریپلای کن.")
        return
    try:
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
            f"🔊 <b>{user.first_name}</b> رفع سکوت شد.",
            parse_mode="HTML"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ خطا: {e}")


# ─── هندلر متنی فارسی ──────────────────────────────────
async def admin_text_handler(update, context):
    text = update.message.text.strip()

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
