import json
import os
from datetime import datetime

FILE = "users.json"


def load() -> dict:
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data: dict):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_user(user) -> dict:
    data = load()
    uid = str(user.id)
    if uid not in data:
        data[uid] = {
            "name": user.first_name,
            "username": user.username or "",
            "coins": 0,
            "level": 1,
            "xp": 0,
            "messages": 0,
            "vip": False,
            "join": datetime.now().strftime("%Y-%m-%d"),
            "bio": "",
        }
        save(data)
    else:
        data[uid]["name"] = user.first_name
        data[uid]["username"] = user.username or ""
        save(data)
    return data[uid]


def add_message(user) -> dict:
    data = load()
    uid = str(user.id)
    if uid not in data:
        get_user(user)
        data = load()
    data[uid]["messages"] = data[uid].get("messages", 0) + 1
    data[uid]["xp"] = data[uid].get("xp", 0) + 2
    xp_needed = data[uid].get("level", 1) * 100
    if data[uid]["xp"] >= xp_needed:
        data[uid]["level"] = data[uid].get("level", 1) + 1
        data[uid]["xp"] = 0
        data[uid]["coins"] = data[uid].get("coins", 0) + 15
    save(data)
    return data[uid]


def add_coin(user, amount: int):
    data = load()
    uid = str(user.id)
    if uid not in data:
        get_user(user)
        data = load()
    data[uid]["coins"] = data[uid].get("coins", 0) + amount
    save(data)


def get_rank_title(level: int) -> str:
    if level >= 100:
        return "🌟 خدای سکتورلند"
    elif level >= 50:
        return "👑 افسانه‌ای"
    elif level >= 30:
        return "💎 الماس"
    elif level >= 20:
        return "🏆 طلایی"
    elif level >= 10:
        return "🥈 نقره‌ای"
    elif level >= 5:
        return "🥉 برنزی"
    else:
        return "🌱 تازه‌کار"


def get_leaderboard(limit: int = 10) -> list:
    data = load()
    return sorted(
        data.items(),
        key=lambda x: (x[1].get("level", 1), x[1].get("messages", 0)),
        reverse=True
    )[:limit]


async def profile_handler(update, context):
    user = update.effective_user
    info = get_user(user)

    level = info.get("level", 1)
    xp = info.get("xp", 0)
    xp_needed = level * 100
    messages = info.get("messages", 0)
    coins = info.get("coins", 0)
    vip = "💎 بله" if info.get("vip") else "❌ خیر"
    rank = get_rank_title(level)
    join = info.get("join", "نامشخص")
    username = f"@{info['username']}" if info.get("username") else "ندارد"
    bio = info.get("bio", "") or "—"

    filled = int((xp / xp_needed) * 10) if xp_needed > 0 else 0
    bar = "█" * filled + "░" * (10 - filled)

    await update.message.reply_text(
        f"👤 <b>پروفایل {user.first_name}</b>\n"
        f"{'━' * 22}\n"
        f"🆔 یوزرنیم: {username}\n"
        f"🏅 رتبه: {rank}\n"
        f"⭐️ لول: {level}\n"
        f"📊 XP: [{bar}] {xp}/{xp_needed}\n"
        f"💬 پیام‌ها: {messages:,}\n"
        f"🪙 سکه: {coins:,}\n"
        f"💎 VIP: {vip}\n"
        f"📅 عضویت: {join}\n"
        f"📝 بیو: {bio}",
        parse_mode="HTML"
    )


async def leaderboard_handler(update, context):
    top = get_leaderboard(10)
    if not top:
        await update.message.reply_text("هنوز کسی در لیست نیست.")
        return

    medals = ["🥇", "🥈", "🥉"]
    text = "🏆 <b>برترین کاربران سکتورلند</b>\n" + "━" * 22 + "\n"
    for i, (uid, info) in enumerate(top):
        medal = medals[i] if i < 3 else f"{i + 1}."
        name = info.get("name", "کاربر")
        level = info.get("level", 1)
        messages = info.get("messages", 0)
        rank = get_rank_title(level)
        text += f"{medal} <b>{name}</b>\n    لول {level} | {rank} | {messages:,} پیام\n"

    await update.message.reply_text(text, parse_mode="HTML")


async def set_bio_handler(update, context):
    user = update.effective_user
    if not context.args:
        await update.message.reply_text(
            "✏️ بیوگرافیت رو بنویس:\n<code>/setbio متن بیوگرافی</code>",
            parse_mode="HTML"
        )
        return
    bio = " ".join(context.args)[:100]
    data = load()
    uid = str(user.id)
    if uid not in data:
        get_user(user)
        data = load()
    data[uid]["bio"] = bio
    save(data)
    await update.message.reply_text(f"✅ بیوگرافی ذخیره شد:\n{bio}")
