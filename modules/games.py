import json
import os
import random
from datetime import datetime

GAMES_FILE = "games.json"


def load():
    if not os.path.exists(GAMES_FILE):
        return {}
    with open(GAMES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data):
    with open(GAMES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_chat_games(chat_id):
    data = load()
    cid = str(chat_id)
    if cid not in data:
        data[cid] = {}
        save(data)
    return data[cid]


def set_chat_game(chat_id, key, value):
    data = load()
    cid = str(chat_id)
    if cid not in data:
        data[cid] = {}
    data[cid][key] = value
    save(data)


def clear_chat_game(chat_id, key):
    data = load()
    cid = str(chat_id)
    if cid in data and key in data[cid]:
        del data[cid][key]
        save(data)


# ─── حدس کلمه ──────────────────────────────────────────
WORDS = [
    ("کامپیوتر", "💻 یه وسیله الکترونیکی که باهاش کار میکنی"),
    ("تلگرام", "📱 اپی که الان توش هستی"),
    ("پیتزا", "🍕 یه غذای ایتالیایی خوشمزه"),
    ("ایران", "🌍 کشور ما"),
    ("دریا", "🌊 آب زیاد و بزرگ"),
    ("هواپیما", "✈️ وسیله نقلیه آسمانی"),
    ("کتاب", "📚 چیزی که توش میخونی"),
    ("آشپزخانه", "🍳 جایی که غذا درست میکنی"),
    ("موبایل", "📱 وسیله ارتباطی همراه"),
    ("برنامه‌نویس", "💻 کسی که کد مینویسه"),
    ("فوتبال", "⚽ ورزش پرطرفدار"),
    ("موسیقی", "🎵 صداهای خوشایند"),
    ("رستوران", "🍽️ جایی که غذا میخوری"),
    ("بیمارستان", "🏥 جایی که مریض‌ها میرن"),
    ("مدرسه", "🏫 جایی که درس میخونی"),
]


async def word_guess_start(update, context):
    chat_id = update.effective_chat.id
    games = get_chat_games(chat_id)

    if games.get("word_guess"):
        await update.message.reply_text("⚠️ یه بازی حدس کلمه در جریانه!")
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
        f"کلمه رو حدس بزن! ({5} شانس داری)",
        parse_mode="HTML"
    )


async def word_guess_check(update, context, guess: str):
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
        # جایزه
        from modules.bank import add_coins_from_message
        for _ in range(20):
            add_coins_from_message(user)
        await update.message.reply_text(
            f"🎉 <b>آفرین {user.first_name}!</b>\n\n"
            f"✅ کلمه درسته: <b>{word}</b>\n"
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

    # نشون دادن حروف درست
    revealed = ""
    for c in word:
        if any(c in g for g in [guess]):
            revealed += c + " "
        else:
            revealed += "_ "

    await update.message.reply_text(
        f"❌ اشتباه! {remaining} شانس دیگه داری\n"
        f"🔤 {revealed}",
        parse_mode="HTML"
    )
    return True


# ─── حدس پرچم ──────────────────────────────────────────
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
    chat_id = update.effective_chat.id
    games = get_chat_games(chat_id)

    if games.get("flag_guess"):
        await update.message.reply_text("⚠️ یه بازی حدس پرچم در جریانه!")
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


# ─── دوئل ───────────────────────────────────────────────
async def duel_start(update, context):
    chat_id = update.effective_chat.id
    user = update.effective_user
    games = get_chat_games(chat_id)

    if not update.message.reply_to_message:
        await update.message.reply_text("⚔️ روی پیام کاربر موردنظر ریپلای کن!")
        return

    target = update.message.reply_to_message.from_user
    if target.id == user.id or target.is_bot:
        await update.message.reply_text("❌ نمیتونی با خودت یا ربات دوئل کنی!")
        return

    if games.get("duel"):
        await update.message.reply_text("⚠️ یه دوئل در جریانه!")
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
        f"{target.first_name} بنویس <b>قبول</b> یا <b>رد</b>",
        parse_mode="HTML"
    )


async def duel_response(update, context, response: str):
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
        # تعیین برنده تصادفی
        winner_id = random.choice([game["challenger"], game["target"]])
        winner_name = game["challenger_name"] if winner_id == game["challenger"] else game["target_name"]
        loser_name = game["target_name"] if winner_id == game["challenger"] else game["challenger_name"]
        loser_id = game["target"] if winner_id == game["challenger"] else game["challenger"]

        clear_chat_game(chat_id, "duel")

        from modules.bank import add_coins_from_message, get_account, update_account
        from telegram import User as TGUser

        # انتقال سکه - ساده
        data_file = "bank.json"
        if os.path.exists(data_file):
            with open(data_file, "r") as f:
                bank_data = json.load(f)

            bet = game["bet"]
            w = str(winner_id)
            l = str(loser_id)

            if l in bank_data and bank_data[l].get("wallet", 0) >= bet:
                bank_data[l]["wallet"] -= bet
                if w not in bank_data:
                    bank_data[w] = {"wallet": 0, "bank": 0, "loan": 0}
                bank_data[w]["wallet"] = bank_data[w].get("wallet", 0) + bet

                with open(data_file, "w") as f:
                    json.dump(bank_data, f, ensure_ascii=False, indent=4)

        rounds = ["🗡 ضربه اول!", "🛡 دفاع کرد!", "⚡ حمله نهایی!"]
        battle = "\n".join(rounds)

        await update.message.reply_text(
            f"⚔️ <b>دوئل شروع شد!</b>\n\n"
            f"{battle}\n\n"
            f"🏆 <b>{winner_name}</b> برنده شد!\n"
            f"😔 {loser_name} باخت\n"
            f"🪙 {game['bet']} سکه منتقل شد!",
            parse_mode="HTML"
        )
        return True

    return False


# ─── دزد و پلیس ─────────────────────────────────────────
COP_ROLES = ["🚔 پلیس", "🦹 دزد"]


async def cop_game_start(update, context):
    chat_id = update.effective_chat.id
    user = update.effective_user
    games = get_chat_games(chat_id)

    if games.get("cop_game"):
        await update.message.reply_text("⚠️ یه بازی دزد و پلیس در جریانه!")
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
    result += "نقش‌ها توی پیوی بهتون گفته میشه!\n"
    result += "پلیس‌ها باید دزدها رو پیدا کنن 🔍"

    await update.message.reply_text(result, parse_mode="HTML")

    # ارسال نقش به صورت خصوصی
    for uid, role in players.items():
        try:
            await context.bot.send_message(
                int(uid),
                f"🎭 نقش تو: <b>{role}</b>\n\n"
                f"{'🚔 وظیفه: دزدها رو پیدا کن!' if 'پلیس' in role else '🦹 وظیفه: از دست پلیس فرار کن!'}",
                parse_mode="HTML"
            )
        except:
            pass

    clear_chat_game(chat_id, "cop_game")
    return True


# ─── هندلر اصلی بازی‌ها ─────────────────────────────────
async def games_handler(update, context):
    text = update.message.text.strip()
    chat_id = update.effective_chat.id
    games = get_chat_games(chat_id)

    # چک بازی‌های فعال
    if games.get("word_guess"):
        result = await word_guess_check(update, context, text)
        if result:
            return

    if games.get("flag_guess"):
        result = await flag_guess_check(update, context, text)
        if result:
            return

    if games.get("duel") and text in ["قبول", "رد"]:
        result = await duel_response(update, context, text)
        if result:
            return

    if games.get("cop_game") and text == "میام":
        result = await cop_join(update, context)
        if result:
            return

    if games.get("cop_game") and text == "شروع دزد":
        result = await cop_game_begin(update, context)
        if result:
            return

