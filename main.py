from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters
)

from modules.fun import (
    get_joke,
    get_fact,
    get_motive,
    get_text,
    get_riddle,
    dice,
    coin,
    rps,
    random_number
)

from modules.admin import (
    warn, clear_warning, warns, setwarnlimit,
    ban, unban, kick, mute, unmute,
    admin_text_handler, get_warn_limit
)

from modules.locks import (
    lock_link, unlock_link, lock_forward, unlock_forward,
    lock_username, unlock_username, lock_photo, unlock_photo,
    lock_video, unlock_video, lock_file, unlock_file,
    lock_sticker, unlock_sticker, check_locks
)

from modules.settings import (
    settings_handler,
    settings_button_handler,
    toggle_setting,
    set_welcome,
    set_rules_handler,
    rules_handler,
    welcome_new_member,
    get
)

from modules.profile import (
    get_user,
    add_message,
    profile_handler,
    leaderboard_handler
)

from modules.useful import (
    useful_handler,
    weather,
    translate,
    calculate,
    convert_unit
)

from modules.bank import (
    bank_profile,
    deposit,
    withdraw,
    daily,
    transfer,
    loan,
    payloan,
    add_coins_from_message
)

from modules.ai import (
    ai_handler,
    smart_ai,
    get_fal,
    ai_ban_reaction,
    ai_kick_reaction,
    ai_warn_reaction
)

from modules.games import (
    word_guess_start,
    flag_guess_start,
    duel_start,
    cop_game_start,
    games_handler
)

from config import TOKEN, BOT_NAME


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


admin_menu = [
    ["⚠️ اخطار", "🧹 پاک اخطار", "📋 اخطارها"],
    ["🚫 بن", "✅ آنبن", "👢 کیک"],
    ["🔇 میوت", "🔊 آنمیوت"],
    ["⚙️ تنظیم حد اخطار"],
    ["🔙 برگشت"]
]


lock_menu = [
    ["قفل لینک", "حذف قفل لینک"],
    ["قفل فوروارد", "حذف قفل فوروارد"],
    ["قفل یوزرنیم", "حذف قفل یوزرنیم"],
    ["قفل عکس", "حذف قفل عکس"],
    ["قفل ویدیو", "حذف قفل ویدیو"],
    ["قفل فایل", "حذف قفل فایل"],
    ["قفل استیکر", "حذف قفل استیکر"],
    ["🔙 برگشت"]
]


bank_menu = [
    ["👛 کیف پول", "🎁 جایزه روزانه"],
    ["🏦 واریز", "💸 برداشت"],
    ["🤝 انتقال سکه", "📛 وام"],
    ["🔙 برگشت"]
]
SETTINGS_BUTTONS = [
    "ضداسپم",
    "فیلتر لینک",
    "فیلتر منشن",
    "خوش‌آمدگویی",
    "✏️ تغییر پیام خوش‌آمد",
    "📜 قوانین گروه"
]


ADMIN_COMMANDS = {
    "اخطار": warn,
    "پاک اخطار": clear_warning,
    "اخطارها": warns,
    "بن": ban,
    "آنبن": unban,
    "کیک": kick,
    "میوت": mute,
    "آنمیوت": unmute,
}


def main_kb():
    return ReplyKeyboardMarkup(
        main_menu,
        resize_keyboard=True
    )


def fun_kb():
    return ReplyKeyboardMarkup(
        fun_menu,
        resize_keyboard=True
    )


def useful_kb():
    return ReplyKeyboardMarkup(
        useful_menu,
        resize_keyboard=True
    )


def admin_kb():
    return ReplyKeyboardMarkup(
        admin_menu,
        resize_keyboard=True
    )


def lock_kb():
    return ReplyKeyboardMarkup(
        lock_menu,
        resize_keyboard=True
    )


def bank_kb():
    return ReplyKeyboardMarkup(
        bank_menu,
        resize_keyboard=True
    )


def clean(text):

    if not text:
        return ""

    emojis = [
        "🎮","🛠","🛡","🔒",
        "👤","🏆","💰",
        "📖","⚙️","🆘",
        "😂","🧠","💪",
        "✨","🎲","🪙",
        "🧩","✂️","🌤",
        "🌐","🔢","📐",
        "⚠️","🚫","✅",
        "👢","🔇","🔊",
        "🔙"
    ]

    for e in emojis:
        text = text.replace(e,"")

    return text.strip()



async def start(update, context):

    user = update.effective_user

    get_user(user)

    await update.message.reply_text(
        f"{BOT_NAME}\n\n"
        f"👋 خوش اومدی {user.first_name}",
        reply_markup=main_kb()
    )



async def menu_handler(update, context):

    text = update.message.text.strip()

    c = clean(text)


    if c in ADMIN_COMMANDS:

        await ADMIN_COMMANDS[c](
            update,
            context
        )

        return



    if c == "تنظیمات":

        await settings_handler(
            update,
            context
        )

        return



    if c == "سرگرمی":

        await update.message.reply_text(
            "🎮 بخش سرگرمی:",
            reply_markup=fun_kb()
        )

        return



    if c == "کاربردی":

        await update.message.reply_text(
            "🛠 بخش کاربردی:",
            reply_markup=useful_kb()
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



    if c in [
        "سنگ",
        "کاغذ",
        "قیچی"
    ]:

        await update.message.reply_text(
            rps(c)
        )

        return



    if c == "پروفایل":

        await profile_handler(
            update,
            context
        )

        return



    if c == "رتبه‌بندی":

        await leaderboard_handler(
            update,
            context
        )

        return



    if c == "سکه و بانک":

        await update.message.reply_text(
            "💰 بانک:",
            reply_markup=bank_kb()
        )

        return



    if c == "کیف پول":

        await bank_profile(
            update,
            context
        )

        return



    if c == "جایزه روزانه":

        await daily(
            update,
            context
        )

        return



    if c == "واریز":

        await update.message.reply_text(
            "🏦 مقدار را بفرست:\n/deposit 100"
        )

        return



    if c == "برداشت":

        await update.message.reply_text(
            "💸 مقدار را بفرست:\n/withdraw 100"
        )

        return



    if c == "حدس کلمه":

        await word_guess_start(
            update,
            context
        )

        return



    if c == "حدس پرچم":

        await flag_guess_start(
            update,
            context
        )

        return



    if c == "دوئل":

        await duel_start(
            update,
            context
        )

        return



    if c == "دزد و پلیس":

        await cop_game_start(
            update,
            context
        )

        return



    if c in [
        "آب و هوا",
        "ترجمه",
        "حساب‌گر",
        "تبدیل واحد"
    ]:

        await useful_handler(
            update,
            context
        )

        return



    # اگر هیچ دکمه‌ای نبود
    if update.effective_chat.type != "private":

        add_message(
            update.effective_user
        )

        add_coins_from_message(
            update.effective_user,
            1
        )
        app = Application.builder().token(TOKEN).build()


app.add_handler(
    CommandHandler(
        "start",
        start
    )
)


app.add_handler(
    CommandHandler(
        "profile",
        profile_handler
    )
)


app.add_handler(
    CommandHandler(
        "top",
        leaderboard_handler
    )
)


app.add_handler(
    CommandHandler(
        "warn",
        warn
    )
)


app.add_handler(
    CommandHandler(
        "ban",
        ban
    )
)


app.add_handler(
    CommandHandler(
        "kick",
        kick
    )
)


app.add_handler(
    CommandHandler(
        "mute",
        mute
    )
)


app.add_handler(
    CommandHandler(
        "unmute",
        unmute
    )
)


app.add_handler(
    CommandHandler(
        "weather",
        weather
    )
)


app.add_handler(
    CommandHandler(
        "translate",
        translate
    )
)


app.add_handler(
    CommandHandler(
        "calc",
        calculate
    )
)


app.add_handler(
    CommandHandler(
        "convert",
        convert_unit
    )
)



# پیام‌های بازی
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        games_handler
    ),
    group=1
)



# منو
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        menu_handler
    ),
    group=2
)



# قفل‌ها
app.add_handler(
    MessageHandler(
        filters.ALL & ~filters.COMMAND,
        check_locks
    ),
    group=3
)



# هوش مصنوعی
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        ai_handler
    ),
    group=4
)



print(
    f"✅ {BOT_NAME} Started!"
)


app.run_polling()
