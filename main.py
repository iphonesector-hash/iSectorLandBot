from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)

from modules.fun import (
    get_joke,
    get_fact,
    get_motive,
    get_text,
    get_riddle,
    dice,
    coin,
    rps
)

from modules.ai import (
    ai_handler,
    smart_ai,
    get_fal
)

from modules.games import (
    games_handler,
    word_guess_start,
    flag_guess_start,
    duel_start,
    cop_game_start
)

from modules.useful import (
    useful_handler,
    weather,
    translate,
    calculate,
    convert_unit
)

from modules.profile import (
    get_user,
    profile_handler,
    leaderboard_handler,
    add_message
)

from modules.bank import (
    bank_profile,
    daily,
    add_coins_from_message
)

from modules.admin import (
    warn,
    clear_warning,
    warns,
    ban,
    unban,
    kick,
    mute,
    unmute,
    setwarnlimit,
    admin_text_handler
)

from modules.settings import (
    settings_handler,
    toggle_setting,
    set_welcome,
    rules_handler,
    set_rules_handler,
    welcome_new_member
)

from modules.locks import (
    check_locks
)

from config import TOKEN, BOT_NAME


OWNER_ID = 5147526780


main_menu = [
    ["🎮 سرگرمی", "🛠 کاربردی"],
    ["🛡 مدیریت", "🔒 قفل‌ها"],
    ["👤 پروفایل", "🏆 رتبه‌بندی"],
    ["💰 سکه و بانک", "📖 فال حافظ"],
    ["⚙️ تنظیمات", "🆘 پشتیبانی"]
]

fun_menu = [
    ["😂 جوک", "🧠 فکت"],
    ["💪 انگیزشی", "✨ متن"],
    ["🎲 تاس", "🪙 شیر یا خط"],
    ["🧩 چیستان", "✂️ سنگ کاغذ قیچی"],
    ["🎯 حدس کلمه", "🏳️ حدس پرچم"],
    ["⚔️ دوئل", "🚔 دزد و پلیس"],
    ["🔙 برگشت"]
]

useful_menu = [
    ["🌤 آب و هوا", "🌐 ترجمه"],
    ["🔢 حساب‌گر", "📐 تبدیل واحد"],
    ["🔙 برگشت"]
]

bank_menu = [
    ["👛 کیف پول", "🎁 جایزه روزانه"],
    ["🔙 برگشت"]
]


def kb(menu):
    return ReplyKeyboardMarkup(
        menu,
        resize_keyboard=True
    )


def clean(text):
    if not text:
        return ""

    emojis = [
        "🎮", "🛠", "🛡", "🔒",
        "👤", "🏆", "💰",
        "📖", "⚙️", "🆘",
        "😂", "🧠", "💪",
        "✨", "🎲", "🪙",
        "🧩", "✂️", "🌤",
        "🌐", "🔢", "📐",
        "🔙"
    ]

    for e in emojis:
        text = text.replace(e, "")

    return text.strip()


async def start(update, context):
    user = update.effective_user
    get_user(user)
    await update.message.reply_text(
        f"{BOT_NAME}\n\n👋 خوش اومدی {user.first_name}",
        reply_markup=kb(main_menu)
    )


async def menu_handler(update, context):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()
    c = clean(text)
    if c == "برگشت":
        await update.message.reply_text(
            "🏠 منوی اصلی:",
            reply_markup=kb(main_menu)
        )
        return
    if c == "سرگرمی":
        await update.message.reply_text(
            "🎮 بخش سرگرمی:",
            reply_markup=kb(fun_menu)
        )
        return

    if c == "کاربردی":
        await update.message.reply_text(
            "🛠 بخش کاربردی:",
            reply_markup=kb(useful_menu)
        )
        return

    if c == "فال حافظ":
        await update.message.reply_text(
            await get_fal(smart_ai),
            parse_mode="HTML"
        )
        return

    if c == "جوک":
        await update.message.reply_text(
            await get_joke(smart_ai)
        )
        return

    if c == "فکت":
        await update.message.reply_text(
            await get_fact(smart_ai)
        )
        return

    if c == "انگیزشی":
        await update.message.reply_text(
            await get_motive(smart_ai)
        )
        return

    if c == "متن":
        await update.message.reply_text(
            await get_text(smart_ai)
        )
        return

    if c == "چیستان":
        await update.message.reply_text(
            await get_riddle(smart_ai),
            parse_mode="HTML"
        )
        return

    if c == "تاس":
        await update.message.reply_text(
            dice()
        )
        return

    if c == "شیر یا خط":
        await update.message.reply_text(
            coin()
        )
        return

    if c == "سنگ کاغذ قیچی":
        await update.message.reply_text(
            "✂️ بنویس: سنگ، کاغذ یا قیچی"
        )
        return

    if c in ["سنگ", "کاغذ", "قیچی"]:
        await update.message.reply_text(
            rps(c)
        )
        return

    if c == "پروفایل":
        await profile_handler(update, context)
        return

    if c == "رتبه‌بندی":
        await leaderboard_handler(update, context)
        return

    if c == "سکه و بانک":
        await update.message.reply_text(
            "💰 بخش بانک:",
            reply_markup=kb(bank_menu)
        )
        return

    if c == "کیف پول":
        await bank_profile(update, context)
        return

    if c == "جایزه روزانه":
        await daily(update, context)
        return

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

    if c in ["آب و هوا", "ترجمه", "حساب‌گر", "تبدیل واحد"]:
        await useful_handler(update, context)
        return

    if update.effective_chat.type != "private":
        add_message(update.effective_user)
        add_coins_from_message(update.effective_user, 1)


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("profile", profile_handler))
app.add_handler(CommandHandler("top", leaderboard_handler))
app.add_handler(CommandHandler("warn", warn))
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("unban", unban))
app.add_handler(CommandHandler("kick", kick))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(CommandHandler("unmute", unmute))
app.add_handler(CommandHandler("weather", weather))
app.add_handler(CommandHandler("translate", translate))
app.add_handler(CommandHandler("calc", calculate))
app.add_handler(CommandHandler("convert", convert_unit))

app.add_handler(
    MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS,
        welcome_new_member
    )
)

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, games_handler),
    group=1
)

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler),
    group=2
)

app.add_handler(
    MessageHandler(filters.ALL & ~filters.COMMAND, check_locks),
    group=3
)

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, ai_handler),
    group=4
)

print(f"✅ {BOT_NAME} Started!")

app.run_polling()
