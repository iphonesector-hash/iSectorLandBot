import json
import os
import random
from datetime import datetime

GAMES_FILE = "games.json"


def load():
    """بارگذاری داده‌های بازی‌ها"""
    if not os.path.exists(GAMES_FILE):
        return {}
    try:
        with open(GAMES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save(data):
    """ذخیره داده‌های بازی‌ها"""
    try:
        with open(GAMES_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        pass


def get_chat_games(chat_id):
    """دریافت بازی‌های گروه"""
    data = load()
    cid = str(chat_id)
    if cid not in data:
        data[cid] = {}
        save(data)
    return data[cid]


def set_chat_game(chat_id, key, value):
    """تنظیم بازی گروه"""
    data = load()
    cid = str(chat_id)
    if cid not in data:
        data[cid] = {}
    data[cid][key] = value
    save(data)


def clear_chat_game(chat_id, key):
    """پاک کردن بازی گروه"""
    data = load()
    cid = str(chat_id)
    if cid in data and key in data[cid]:
        del data[cid][key]
        save(data)


# ═══════════════════════════════════════════════════════════
# حدس کلمه
# ═══════════════════════════════════════════════════════════

WORDS = [
    ("کامپیوتر", "💻 یک وسیله الکترونیکی"),
    ("تلگرام", "📱 اپ پیامی شهیر"),
    ("پیتزا", "🍕 غذای ایتالیایی"),
    ("ایران", "🌍 کشور ما"),
    ("دریا", "🌊 آب زیاد و بزرگ"),
    ("هواپیما", "✈️ وسیله نقلیه آسمانی"),
    ("کتاب", "📚 منبع دانش"),
    ("آشپزخانه", "🍳 جایی که غذا درست میشود"),
    ("موبایل", "📱 وسیله ارتباطی"),
    ("برنامه‌نویس", "💻 کسی که کد مینویسد"),
    ("فوتبال", "⚽ ورزش پرطرفدار"),
    ("موسیقی", "🎵 هنر صدا"),
    ("رستوران", "🍽️ جایی برای خوردن"),
    ("بیمارستان", "🏥 جای درمان بیماری"),
    ("مدرسه", "🏫 جایی برای یادگیری"),
]


async def word_guess_start(update, context):
    """شروع بازی حدس کلمه"""
    chat_id = update.effective_chat.id
    games = get_chat_games(chat_id)

    if games.get("word_guess"):
        await update.message.reply_text("⚠️ یک بازی حدس کلمه در جریان است!")
        return

    word, hint = random.choice(WORDS)
    hidden = "_ " * len(word)

    set_chat_game(chat_id, "word_guess", {
        "word": word,
        "hint": hint,
        "tries": 0,
        "max_tries": 5,
        "starter": update.effective_user.id
    })

    await update.message.reply_text(
        f"🎯 <b>بازی حدس کلمه شروع شد!</b>\n\n"
        f"💡 راهنما: {hint}\n"
        f"🔤 کلمه: {hidden}\n"
        f"📏 تعداد حروف: {len(word)}\n\n"
        f"کلمه رو حدس بزن! (5 شانس داری)",
        parse_mode="HTML"
    )


async def word_guess_check(update, context, guess: str):
    """چک کردن جواب حدس کلمه"""
    chat_id = update.effective_chat.id
    user = update.effective_user
    games = get_chat_games(chat_id)
    game = games.get("word_guess")

    if not game:
        return False

    guess = guess.strip()
    word = game["word"]
    game["tries"] += 1

    if guess == word:
        clear_chat_game(chat_id, "word_guess")
        from modules.bank import add_coins_from_message
        for _ in range(20):
            add_coins_from_message(user)
        await update.message.reply_text(
            f"🎉 <b>آفرین {user.first_name}!</b>\n\n"
            f"✅ کلمه درست: <b>{word}</b>\n"
            f"🪙 +20 سکه جایزه گرفتی!",
            parse_mode="HTML"
        )
        return True

    if game["tries"] >= game["max_tries"]:
        clear_chat_game(chat_id, "word_guess")
        await update.message.reply_text(
            f"😔 بازی تموم شد!\n"
            f"کلمه درست: <b>{word}</b>",
            parse_mode="HTML"
        )
        return True

    remaining = game["max_tries"] - game["tries"]
    set_chat_game(chat_id, "word_guess", game)

    revealed = ""
    for c in word:
        if c in guess:
            revealed += c + " "
        else:
            revealed += "_ "

    await update.message.reply_text(
        f"❌ اشتباه! {remaining} شانس دیگه داری\n"
        f"🔤 {revealed}",
        parse_mode="HTML"
    )
    return True


# ═══════════════════════════════════════════════════════════
# حدس پرچم
# ═══════════════════════════════════════════════════════════

FLAGS = [
    ("🇮🇷", "ایران"), ("🇺🇸", "آمریکا"), ("🇬🇧", "انگلیس"),
    ("🇩🇪", "آلمان"), ("🇫🇷", "فرانسه"), ("🇯🇵", "ژاپن"),
    ("🇨🇳", "چین"), ("🇷🇺", "روسیه"), ("🇮🇹", "ایتالیا"),
    ("🇸🇦", "عربستان"), ("🇹🇷", "ترکیه"), ("🇦🇪", "امارات"),
    ("🇧🇷", "برزیل"), ("🇦🇺", "استرالیا"), ("🇨🇦", "کانادا"),
    ("🇰🇷", "کره جنوبی"), ("🇮🇳", "هند"), ("🇲🇽", "مکزیک"),
    ("🇵🇰", "پاکستان"), ("🇪🇸", "اسپانیا"),
]


async def flag_guess_start(update, context):
    """شروع بازی حدس پرچم"""
    chat_id = update.effective_chat.id
    games = get_chat_games(chat_id)

    if games.get("flag_guess"):
        await update.message.reply_text("⚠️ یک بازی حدس پرچم در جریان است!")
        return

    flag, country = random.choice(FLAGS)
    set_chat_game(chat_id, "flag_guess", {
        "flag": flag,
        "country": country,
        "tries": 0
    })

    await update.message.reply_text(
        f"🏳️ <b>این پرچم کدوم کشوره؟</b>\n\n"
        f"{flag}\n\n"
        f"اسم کشور رو فارسی بنویس!",
        parse_mode="HTML"
    )


async def flag_guess_check(update, context, guess: str):
    """چک کردن جواب حدس پرچم"""
    chat_id = update.effective_chat.id
    user = update.effective_user
    games = get_chat_games(chat_id)
    game = games.get("flag_guess")

    if not game:
        return False

    guess = guess.strip()
    country = game["country"]
    game["tries"] += 1

    if guess == country:
        clear_chat_game(chat_id, "flag_guess")
        from modules.bank import add_coins_from_message
        for _ in range(10):
            add_coins_from_message(user)
        await update.message.reply_text(
            f"🎉 درسته! پرچم <b>{country}</b> {game['flag']}\n"
            f"🪙 +10 سکه جایزه!",
            parse_mode="HTML"
        )
        return True

    if game["tries"] >= 3:
        clear_chat_game(chat_id, "flag_guess")
        await update.message.reply_text(
            f"😔 جواب درست: <b>{country}</b> {game['flag']}"
        )
        return True

    set_chat_game(chat_id, "flag_guess", game)
    await update.message.reply_text(f"❌ اشتباه! {3 - game['tries']} شانس دیگه")
    return True


# ═══════════════════════════════════════════════════════════
# دوئل
# ═══════════════════════════════════════════════════════════

async def duel_start(update, context):
    """شروع دوئل"""
    chat_id = update.effective_chat.id
    user = update.effective_user
    games = get_chat_games(chat_id)

    if not update.message.reply_to_message:
        await update.message.reply_text("⚔️ روی پیام کاربر دوئل رو دعوت کن!")
        return

    target = update.message.reply_to_message.from_user
    if target.id == user.id or target.is_bot:
        await update.message.reply_text("❌ نمیتونی با خودت یا ربات دوئل کنی!")
        return

    if games.get("duel"):
        await update.message.reply_text("⚠️ یک دوئل در جریان است!")
        return

    bet = 20
    set_chat_game(chat_id, "duel", {
        "challenger": user.id,
        "challenger_name": user.first_name,
        "target": target.id,
        "target_name": target.first_name,
        "bet": bet
    })

    await update.message.reply_text(
        f"⚔️ <b>{user.first_name}</b> به <b>{target.first_name}</b> دوئل داد!\n\n"
        f"💰 شرط: {bet} سکه\n\n"
        f"@{target.username or target.first_name} بنویس: <b>قبول</b> یا <b>رد</b>",
        parse_mode="HTML"
    )


async def duel_response(update, context, response: str):
    """پاسخ به دوئل"""
    chat_id = update.effective_chat.id
    user = update.effective_user
    games = get_chat_games(chat_id)
    game = games.get("duel")

    if not game or user.id != game["target"]:
        return False

    if response == "رد":
        clear_chat_game(chat_id, "duel")
        await update.message.reply_text(
            f"🏳️ {user.first_name} دوئل رو رد کرد!"
        )
        return True

    if response == "قبول":
        winner_id = random.choice([game["challenger"], game["target"]])
        winner_name = game["challenger_name"] if winner_id == game["challenger"] else game["target_name"]
        loser_name = game["target_name"] if winner_id == game["challenger"] else game["challenger_name"]
        loser_id = game["target"] if winner_id == game["challenger"] else game["challenger"]

        clear_chat_game(chat_id, "duel")

        from modules.bank import get_account, update_account
        
        winner_acc = get_account(type('obj', (object,), {'id': winner_id})())
        loser_acc = get_account(type('obj', (object,), {'id': loser_id})())
        
        bet = game["bet"]
        if loser_acc["wallet"] >= bet:
            loser_acc["wallet"] -= bet
            winner_acc["wallet"] += bet
            update_account(loser_id, loser_acc)
            update_account(winner_id, winner_acc)

        await update.message.reply_text(
            f"⚔️ <b>دوئل شروع شد!</b>\n\n"
            f"🗡️ ضربه اول!\n"
            f"🛡️ دفاع کرد!\n"
            f"⚡ حمله نهایی!\n\n"
            f"🏆 <b>{winner_name}</b> برنده شد!\n"
            f"😔 {loser_name} باخت\n"
            f"🪙 {bet} سکه منتقل شد!",
            parse_mode="HTML"
        )
        return True

    return False


# ═══════════════════════════════════════════════════════════
# دزد و پلیس
# ═══════════════════════════════════════════════════════════

COP_ROLES = ["🚔 پلیس", "🦹 دزد"]


async def cop_game_start(update, context):
    """شروع بازی دزد و پلیس"""
    chat_id = update.effective_chat.id
    user = update.effective_user
    games = get_chat_games(chat_id)

    if games.get("cop_game"):
        await update.message.reply_text("⚠️ یک بازی دزد و پلیس در جریان است!")
        return

    role = random.choice(COP_ROLES)
    set_chat_game(chat_id, "cop_game", {
        "players": {str(user.id): role},
        "starter": user.id,
        "started": False
    })

    await update.message.reply_text(
        f"🚔 <b>بازی دزد و پلیس!</b>\n\n"
        f"برای پیوستن بنویس: <b>میام</b>\n"
        f"وقتی همه اومدن بنویس: <b>شروع دزد</b>",
        parse_mode="HTML"
    )


async def cop_join(update, context):
    """پیوستن به بازی"""
    chat_id = update.effective_chat.id
    user = update.effective_user
    games = get_chat_games(chat_id)
    game = games.get("cop_game")

    if not game or game.get("started"):
        return False

    if str(user.id) in game["players"]:
        await update.message.reply_text("✅ قبلاً پیوستی!")
        return True

    role = random.choice(COP_ROLES)
    game["players"][str(user.id)] = role
    set_chat_game(chat_id, "cop_game", game)

    await update.message.reply_text(
        f"✅ {user.first_name} پیوست! ({len(game['players'])} نفر)"
    )
    return True


async def cop_game_begin(update, context):
    """شروع بازی"""
    chat_id = update.effective_chat.id
    user = update.effective_user
    games = get_chat_games(chat_id)
    game = games.get("cop_game")

    if not game or game["starter"] != user.id:
        return False

    players = game["players"]
    if len(players) < 2:
        await update.message.reply_text("❌ حداقل ۲ نفر لازمه!")
        return True

    game["started"] = True
    set_chat_game(chat_id, "cop_game", game)

    result = "🎭 <b>نقش‌ها تعیین شد!</b>\n\n"
    cops = []
    thieves = []

    for uid, role in players.items():
        if "پلیس" in role:
            cops.append(uid)
        else:
            thieves.append(uid)

    result += f"🚔 پلیس‌ها: {len(cops)} نفر\n"
    result += f"🦹 دزدها: {len(thieves)} نفر\n\n"
    result += "پلیس‌ها باید دزدها رو پیدا کنن 🔍"

    await update.message.reply_text(result, parse_mode="HTML")

    clear_chat_game(chat_id, "cop_game")
    return True


# ═══════════════════════════════════════════════════════════
# هندلر اصلی بازی‌ها
# ═══════════════════════════════════════════════════════════

async def games_handler(update, context):
    """هندلر اصلی بازی‌ها"""
    if not update.message or not update.message.text:
        return
    
    text = update.message.text.strip()
    chat_id = update.effective_chat.id
    games = get_chat_games(chat_id)

    # بازی حدس کلمه
    if games.get("word_guess"):
        result = await word_guess_check(update, context, text)
        if result:
            return

    # بازی حدس پرچم
    if games.get("flag_guess"):
        result = await flag_guess_check(update, context, text)
        if result:
            return

    # بازی دوئل
    if games.get("duel") and text in ["قبول", "رد"]:
        result = await duel_response(update, context, text)
        if result:
            return

    # بازی دزد و پلیس - پیوستن
    if games.get("cop_game") and text == "میام":
        result = await cop_join(update, context)
        if result:
            return

    # بازی دزد و پلیس - شروع
    if games.get("cop_game") and text == "شروع دزد":
        result = await cop_game_begin(update, context)
        if result:
            return
