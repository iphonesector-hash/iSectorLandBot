from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from modules.fun import get_joke, get_fact, get_motive, get_text, get_riddle, get_fal, dice, coin, rps
from modules.ai import ai_handler
from modules.games import games_handler, word_guess_start, flag_guess_start, duel_start, cop_game_start
from modules.useful import useful_handler, weather, translate, calculate, convert_unit
from modules.profile import get_user, profile_handler, leaderboard_handler, add_message, set_bio_handler
from modules.bank import (
    bank_profile, daily, add_coins_from_message,
    deposit, withdraw, transfer, loan, payloan, rich_leaderboard
)
from modules.admin import warn, clear_warning, warns, ban, unban, kick, mute, unmute, setwarnlimit
from modules.settings import (
    welcome_new_member, settings_handler, set_welcome,
    set_rules_handler, rules_handler, toggle_setting, get, set_option
)
from modules.locks import (
    check_locks, show_locks_status, unlock_all,
    lock_link, lock_photo, lock_video, lock_audio,
    lock_sticker, lock_gif, lock_file, lock_forward, lock_text
)
from config import TOKEN, BOT_NAME, SUPPORT_USERNAME

# ─── منوها ──────────────────────────────────────────────
MAIN_MENU = [
    ["🎮 سرگرمی", "🛠 کاربردی"],
    ["🛡 مدیریت", "🔒 قفل‌ها"],
    ["👤 پروفایل", "🏆 رتبه‌بندی"],
    ["💰 سکه و بانک", "📖 فال حافظ"],
    ["⚙️ تنظیمات", "🆘 پشتیبانی"],
]
FUN_MENU = [
    ["😂 جوک", "🧠 فکت"],
    ["💪 انگیزشی", "✨ متن"],
    ["🎲 تاس", "🪙 شیر یا خط"],
    ["🧩 چیستان", "✂️ سنگ کاغذ قیچی"],
    ["🎯 حدس کلمه", "🏳️ حدس پرچم"],
    ["⚔️ دوئل", "🚔 دزد و پلیس"],
    ["🔙 برگشت"],
]
USEFUL_MENU = [
    ["🌤 آب و هوا", "🌐 ترجمه"],
    ["🔢 حساب‌گر", "📐 تبدیل واحد"],
    ["🔙 برگشت"],
]
ADMIN_MENU = [
    ["⚠️ اخطار", "📋 اخطارها"],
    ["👢 اخراج", "🚫 بن"],
    ["🔓 آن‌بن", "🔇 سکوت"],
    ["🔊 رفع سکوت", "📢 پیام همگانی"],
    ["🔙 برگشت"],
]
LOCKS_MENU = [
    ["🔗 قفل لینک", "🖼 قفل عکس"],
    ["🎬 قفل فیلم", "🎵 قفل آهنگ"],
    ["🧩 قفل استیکر", "🎞 قفل گیف"],
    ["📎 قفل فایل", "↪️ قفل فوروارد"],
    ["💬 قفل متن", "📊 وضعیت قفل‌ها"],
    ["🔓 باز کردن همه"],
    ["🔙 برگشت"],
]
BANK_MENU = [
    ["👛 کیف پول", "🎁 جایزه روزانه"],
    ["🏦 واریز به بانک", "💸 برداشت از بانک"],
    ["🤝 انتقال سکه", "📊 ثروتمندترین‌ها"],
    ["💳 وام", "✅ پرداخت وام"],
    ["🔙 برگشت"],
]


def kb(menu):
    return ReplyKeyboardMarkup(menu, resize_keyboard=True)


def clean(text: str) -> str:
    if not text:
        return ""
    emojis = [
        "🎮","🛠","🛡","🔒","👤","🏆","💰","📖","⚙️","🆘",
        "😂","🧠","💪","✨","🎲","🪙","🧩","✂️","🌤","🌐",
        "🔢","📐","🔙","⚠️","📋","👢","🚫","🔓","🔇","🔊",
        "📢","🔗","🖼","🎬","🎵","🎞","📎","↪️","💬","👋",
        "🎯","🏳️","⚔️","🚔","👛","🎁","🏦","💸","🤝","📊",
        "💳","✅","🔔","✏️",
    ]
    for e in emojis:
        text = text.replace(e, "")
    return text.strip()


# ─── استارت ─────────────────────────────────────────────
async def start(update, context):
    user = update.effective_user
    get_user(user)
    await update.message.reply_text(
        f"{BOT_NAME}\n\n👋 خوش اومدی <b>{user.first_name}</b> 🌻\n\n"
        f"از منوی زیر یه بخش رو انتخاب کن:",
        reply_markup=kb(MAIN_MENU),
        parse_mode="HTML"
    )


# ─── هندلر اصلی منو ─────────────────────────────────────
async def menu_handler(update, context):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()
    c = clean(text)
    chat = update.effective_chat
    user = update.effective_user

    # ─── ثبت پیام و سکه اول از همه ───
    if chat and chat.type != "private":
        add_message(user)
        add_coins_from_message(user, 1)

    # ─── ضد اسپم و فیلتر لینک از تنظیمات ───
    if chat and chat.type != "private":
        cfg = get(chat.id)
        import time
        if cfg.get("spam"):
            now = time.time()
            last = context.chat_data.get(f"spam_{user.id}", 0)
            if now - last < 2:
                try:
                    await update.message.delete()
                except Exception:
                    pass
                return
            context.chat_data[f"spam_{user.id}"] = now
        if cfg.get("link") and ("http" in text or "t.me/" in text):
            try:
                await update.message.delete()
                await update.message.reply_text("🚫 ارسال لینک در این گروه ممنوع است.")
            except Exception:
                pass
            return
        if cfg.get("mention") and text.count("@") >= 2:
            try:
                await update.message.delete()
                await update.message.reply_text("🚫 منشن زیاد ممنوع است.")
            except Exception:
                pass
            return

    # ─── برگشت ───
    if c == "برگشت":
        await update.message.reply_text("🏠 منوی اصلی:", reply_markup=kb(MAIN_MENU))
        return

    # ─── منوها ───
    if c == "سرگرمی":
        await update.message.reply_text("🎮 بخش سرگرمی:", reply_markup=kb(FUN_MENU))
        return
    if c == "کاربردی":
        await update.message.reply_text("🛠 بخش کاربردی:", reply_markup=kb(USEFUL_MENU))
        return
    if c == "مدیریت":
        await update.message.reply_text("🛡 پنل مدیریت:", reply_markup=kb(ADMIN_MENU))
        return
    if c == "قفل‌ها":
        await update.message.reply_text("🔒 تنظیمات قفل گروه:", reply_markup=kb(LOCKS_MENU))
        return
    if c == "تنظیمات":
        await settings_handler(update, context)
        return
    if c == "پشتیبانی":
        support_btn = InlineKeyboardMarkup([[
            InlineKeyboardButton("💬 پشتیبانی سکتورلند", url=f"https://t.me/{SUPPORT_USERNAME}")
        ]])
        await update.message.reply_text(
            "🆘 <b>پشتیبانی سکتورلند</b>\n\nبرای ارتباط روی دکمه زیر بزن 👇",
            reply_markup=support_btn,
            parse_mode="HTML"
        )
        return

    # ─── فال حافظ ───
    if c == "فال حافظ":
        await context.bot.send_chat_action(update.effective_chat.id, "typing")
        try:
            result = await get_fal()
            await update.message.reply_text(result)
        except Exception:
            await update.message.reply_text("📖 فال حافظ آماده نشد 🌹 دوباره امتحان کن.")
        return

    # ─── سرگرمی ───
    if c == "جوک":
        await context.bot.send_chat_action(update.effective_chat.id, "typing")
        await update.message.reply_text(await get_joke())
        return
    if c == "فکت":
        await context.bot.send_chat_action(update.effective_chat.id, "typing")
        await update.message.reply_text(await get_fact())
        return
    if c == "انگیزشی":
        await context.bot.send_chat_action(update.effective_chat.id, "typing")
        await update.message.reply_text(await get_motive())
        return
    if c == "متن":
        await context.bot.send_chat_action(update.effective_chat.id, "typing")
        await update.message.reply_text(await get_text())
        return
    if c == "چیستان":
        await context.bot.send_chat_action(update.effective_chat.id, "typing")
        await update.message.reply_text(await get_riddle())
        return
    if c == "تاس":
        await update.message.reply_text(dice())
        return
    if c == "شیر یا خط":
        await update.message.reply_text(coin())
        return
    if c == "سنگ کاغذ قیچی":
        await update.message.reply_text("✂️ بنویس: سنگ، کاغذ یا قیچی")
        return
    if c in ["سنگ", "کاغذ", "قیچی"]:
        await update.message.reply_text(rps(c))
        return

    # ─── پروفایل ───
    if c == "پروفایل":
        await profile_handler(update, context)
        return
    if c == "رتبه‌بندی":
        await leaderboard_handler(update, context)
        return

    # ─── بانک ───
    if c == "سکه و بانک":
        await update.message.reply_text("💰 بخش بانک:", reply_markup=kb(BANK_MENU))
        return
    if c == "کیف پول":
        await bank_profile(update, context)
        return
    if c == "جایزه روزانه":
        await daily(update, context)
        return
    if c == "واریز به بانک":
        await update.message.reply_text("🏦 مقدار واریز:\n<code>/deposit 100</code>", parse_mode="HTML")
        return
    if c == "برداشت از بانک":
        await update.message.reply_text("💸 مقدار برداشت:\n<code>/withdraw 100</code>", parse_mode="HTML")
        return
    if c == "انتقال سکه":
        await update.message.reply_text("🤝 روی پیام کاربر ریپلای کن:\n<code>/transfer 100</code>", parse_mode="HTML")
        return
    if c == "ثروتمندترین‌ها":
        await rich_leaderboard(update, context)
        return
    if c == "وام":
        await update.message.reply_text("💳 مقدار وام:\n<code>/loan 200</code>", parse_mode="HTML")
        return
    if c == "پرداخت وام":
        await payloan(update, context)
        return

    # ─── مدیریت ───
    if c == "اخطار":
        await warn(update, context)
        return
    if c == "اخطارها":
        await warns(update, context)
        return
    if c == "اخراج":
        await kick(update, context)
        return
    if c == "بن":
        await ban(update, context)
        return
    if c == "آن‌بن":
        await unban(update, context)
        return
    if c == "سکوت":
        await mute(update, context)
        return
    if c == "رفع سکوت":
        await unmute(update, context)
        return
    if c == "پیام همگانی":
        await update.message.reply_text("📢 متن پیام:\n<code>/broadcast متن</code>", parse_mode="HTML")
        return

    # ─── قفل‌ها ───
    lock_map = {
        "قفل لینک": lock_link,
        "قفل عکس": lock_photo,
        "قفل فیلم": lock_video,
        "قفل آهنگ": lock_audio,
        "قفل استیکر": lock_sticker,
        "قفل گیف": lock_gif,
        "قفل فایل": lock_file,
        "قفل فوروارد": lock_forward,
        "قفل متن": lock_text,
    }
    if c in lock_map:
        await lock_map[c](update, context)
        return
    if c == "وضعیت قفل‌ها":
        await show_locks_status(update, context)
        return
    if c == "باز کردن همه":
        await unlock_all(update, context)
        return

    # ─── تنظیمات (دکمه‌های toggle) ───
    settings_triggers = ["خوش‌آمدگویی", "ضد لینک", "ضد اسپم", "فیلتر منشن", "قوانین گروه", "تغییر پیام خوش‌آمد"]
    if c in settings_triggers or "روشن کن" in text or "خاموش کن" in text:
        from modules.settings import settings_button_handler
        await settings_button_handler(update, context)
        return

    # ─── بازی‌ها ───
    if c == "حدس کلمه":
        await word_guess_start(update, context)
        return
    if c == "حدس پرچم":
        await flag_guess_start(update, context)
        return
    if c == "دوئل":
        await duel_start(update, context)
        return
    if c == "دزد و پلیس":
        await cop_game_start(update, context)
        return

    # ─── کاربردی ───
    if c in ["آب و هوا", "ترجمه", "حساب‌گر", "تبدیل واحد"]:
        await useful_handler(update, context)
        return


# ─── ساخت اپ ────────────────────────────────────────────
app = Application.builder().token(TOKEN).build()

# ─── دستورات ────────────────────────────────────────────
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("profile", profile_handler))
app.add_handler(CommandHandler("top", leaderboard_handler))
app.add_handler(CommandHandler("setbio", set_bio_handler))
app.add_handler(CommandHandler("warn", warn))
app.add_handler(CommandHandler("clearwarn", clear_warning))
app.add_handler(CommandHandler("warns", warns))
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("unban", unban))
app.add_handler(CommandHandler("kick", kick))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(CommandHandler("unmute", unmute))
app.add_handler(CommandHandler("setwarnlimit", setwarnlimit))
app.add_handler(CommandHandler("weather", weather))
app.add_handler(CommandHandler("translate", translate))
app.add_handler(CommandHandler("calc", calculate))
app.add_handler(CommandHandler("convert", convert_unit))
app.add_handler(CommandHandler("deposit", deposit))
app.add_handler(CommandHandler("withdraw", withdraw))
app.add_handler(CommandHandler("transfer", transfer))
app.add_handler(CommandHandler("loan", loan))
app.add_handler(CommandHandler("payloan", payloan))
app.add_handler(CommandHandler("setwelcome", set_welcome))
app.add_handler(CommandHandler("setrules", set_rules_handler))
app.add_handler(CommandHandler("rules", rules_handler))
app.add_handler(CommandHandler("toggle", toggle_setting))
app.add_handler(CommandHandler("locks", show_locks_status))

# ─── عضو جدید ───────────────────────────────────────────
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))

# ─── قفل‌ها — اول از همه (group=0) ──────────────────────
app.add_handler(
    MessageHandler(filters.ALL & ~filters.COMMAND, check_locks),
    group=0
)

# ─── منو (group=1) ──────────────────────────────────────
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler),
    group=1
)

# ─── بازی‌ها (group=2) ──────────────────────────────────
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, games_handler),
    group=2
)

# ─── AI فقط در پیوی (group=3) ───────────────────────────
app.add_handler(
    MessageHandler(
        filters.TEXT & filters.ChatType.PRIVATE & ~filters.COMMAND,
        ai_handler
    ),
    group=3
)

print(f"✅ {BOT_NAME} Started!")
app.run_polling(drop_pending_updates=True)
