import json
import os
from datetime import datetime

FILE = "users.json"


def load():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)


def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_user(user):
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
            "join": str(datetime.now().strftime("%Y-%m-%d"))
        }
        save(data)
    else:
        # آپدیت اسم در صورت تغییر
        data[uid]["name"] = user.first_name
        save(data)
    return data[uid]


def add_message(user):
    """هر بار که کاربر پیام بفرسته صدا زده میشه"""
    data = load()
    uid = str(user.id)

    if uid not in data:
        get_user(user)
        data = load()

    data[uid]["messages"] = data[uid].get("messages", 0) + 1
    data[uid]["xp"] = data[uid].get("xp", 0) + 1

    # هر ۱۰۰ XP یه لول بالا
    xp_needed = data[uid]["level"] * 100
    if data[uid]["xp"] >= xp_needed:
        data[uid]["level"] += 1
        data[uid]["xp"] = 0
        data[uid]["coins"] = data[uid].get("coins", 0) + 10

    save(data)
    return data[uid]


def add_coin(user, amount):
    data = load()
    uid = str(user.id)
    if uid not in data:
        get_user(user)
        data = load()
    data[uid]["coins"] = data[uid].get("coins", 0) + amount
    save(data)


def get_rank_title(level):
    if level >= 50:
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


def get_leaderboard(limit=10):
    data = load()
    sorted_users = sorted(
        data.items(),
        key=lambda x: (x[1].get("level", 1), x[1].get("messages", 0)),
        reverse=True
    )
    return sorted_users[:limit]


async def profile_handler(update, context):
    user = update.effective_user
    info = get_user(user)

    level = info.get("level", 1)
    xp = info.get("xp", 0)
    xp_needed = level * 100
    messages = info.get("messages", 0)
    coins = info.get("coins", 0)
    vip = "✅ بله" if info.get("vip") else "❌ خیر"
    rank = get_rank_title(level)
    join = info.get("join", "نامشخص")

    # نوار پیشرفت XP
    filled = int((xp / xp_needed) * 10)
    bar = "█" * filled + "░" * (10 - filled)

    await update.message.reply_text(
        f"👤 <b>پروفایل {user.first_name}</b>\n"
        f"{'─' * 25}\n"
        f"🏅 رتبه: {rank}\n"
        f"⭐ لول: {level}\n"
        f"📊 XP: [{bar}] {xp}/{xp_needed}\n"
        f"💬 پیام‌ها: {messages}\n"
        f"🪙 سکه: {coins}\n"
        f"💎 VIP: {vip}\n"
        f"📅 تاریخ عضویت: {join}\n",
        parse_mode="HTML"
    )


async def leaderboard_handler(update, context):
    top = get_leaderboard(10)

    if not top:
        await update.message.reply_text("هنوز کسی در لیست نیست.")
        return

    medals = ["🥇", "🥈", "🥉"]
    text = "🏆 <b>برترین کاربران گروه</b>\n" + "─" * 25 + "\n"

    for i, (uid, info) in enumerate(top):
        medal = medals[i] if i < 3 else f"{i+1}."
        name = info.get("name", "کاربر")
        level = info.get("level", 1)
        messages = info.get("messages", 0)
        rank = get_rank_title(level)
        text += f"{medal} <b>{name}</b> | لول {level} | {rank} | {messages} پیام\n"

    await update.message.reply_text(text, parse_mode="HTML")
