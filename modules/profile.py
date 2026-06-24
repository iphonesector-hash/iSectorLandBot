import json
import os
from datetime import datetime

USERS_FILE = "users.json"


def load():
    """بارگذاری اطلاعات کاربران"""
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save(data):
    """ذخیره اطلاعات کاربران"""
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        pass


def get_user(user):
    """دریافت یا ایجاد کاربر"""
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
            "vip_expire": "",
            "join": str(datetime.now().strftime("%Y-%m-%d")),
            "achievements": []
        }
        save(data)
    else:
        data[uid]["name"] = user.first_name
        save(data)
    return data[uid]


def add_message(user):
    """اضافه کردن پیام و XP"""
    data = load()
    uid = str(user.id)

    if uid not in data:
        get_user(user)
        data = load()

    data[uid]["messages"] = data[uid].get("messages", 0) + 1
    data[uid]["xp"] = data[uid].get("xp", 0) + 1

    # هر 100 XP یک لول بالا
    xp_needed = data[uid]["level"] * 100
    if data[uid]["xp"] >= xp_needed:
        data[uid]["level"] += 1
        data[uid]["xp"] = 0
        data[uid]["coins"] = data[uid].get("coins", 0) + 25

    save(data)
    return data[uid]


def get_rank_title(level):
    """دریافت عنوان رتبه بر اساس لول"""
    if level >= 100:
        return "👑 افسانه‌ای"
    elif level >= 50:
        return "💎 الماس"
    elif level >= 30:
        return "🏆 طلایی"
    elif level >= 20:
        return "🥈 نقره‌ای"
    elif level >= 10:
        return "🥉 برنزی"
    elif level >= 5:
        return "⭐ ستاره"
    else:
        return "🌱 تازه‌کار"


def get_rank_color(level):
    """رنگ بندی رتبه‌ها"""
    if level >= 100:
        return "👑"
    elif level >= 50:
        return "💎"
    elif level >= 30:
        return "🏆"
    elif level >= 20:
        return "🥈"
    elif level >= 10:
        return "🥉"
    else:
        return "⭐"


def get_leaderboard(limit=15):
    """دریافت برترین کاربران"""
    data = load()
    sorted_users = sorted(
        data.items(),
        key=lambda x: (x[1].get("level", 1), x[1].get("xp", 0), x[1].get("messages", 0)),
        reverse=True
    )
    return sorted_users[:limit]


async def profile_handler(update, context):
    """نمایش پروفایل کاربر"""
    user = update.effective_user
    info = get_user(user)

    level = info.get("level", 1)
    xp = info.get("xp", 0)
    xp_needed = level * 100
    messages = info.get("messages", 0)
    coins = info.get("coins", 0)
    vip = "✅ بله" if info.get("vip") else "❌ خیر"
    rank = get_rank_title(level)
    rank_icon = get_rank_color(level)
    join = info.get("join", "نامشخص")

    # نوار پیشرفت XP
    filled = int((xp / xp_needed) * 15)
    bar = "█" * filled + "░" * (15 - filled)

    # محاسبه تا لول بعدی
    progress_percent = int((xp / xp_needed) * 100)

    await update.message.reply_text(
        f"👤 <b>پروفایل {user.first_name}</b>\n"
        f"{'═' * 35}\n\n"
        f"{rank_icon} <b>رتبه:</b> {rank}\n"
        f"⭐ <b>لول:</b> {level}\n"
        f"📊 <b>تجربه:</b> [{bar}] {progress_percent}%\n"
        f"   └─ {xp}/{xp_needed} XP\n"
        f"💬 <b>پیام‌ها:</b> {messages:,}\n"
        f"🪙 <b>سکه‌ها:</b> {coins:,}\n"
        f"💎 <b>VIP:</b> {vip}\n"
        f"📅 <b>عضویت:</b> {join}\n"
        f"{'═' * 35}",
        parse_mode="HTML"
    )


async def leaderboard_handler(update, context):
    """نمایش رتبه‌بندی"""
    top = get_leaderboard(15)

    if not top:
        await update.message.reply_text("هنوز کسی در لیست نیست.")
        return

    medals = ["🥇", "🥈", "🥉"]
    text = (
        "🏆 <b>برترین کاربران گروه</b>\n"
        "═" * 40 + "\n\n"
    )

    for i, (uid, info) in enumerate(top):
        medal = medals[i] if i < 3 else f"{i+1}️⃣"
        name = info.get("name", "کاربر")
        level = info.get("level", 1)
        messages = info.get("messages", 0)
        xp = info.get("xp", 0)
        rank = get_rank_title(level)
        vip_badge = "💎" if info.get("vip") else ""

        text += (
            f"{medal} <b>{name}</b> {vip_badge}\n"
            f"   ├─ لول: {level} | رتبه: {rank}\n"
            f"   ├─ پیام: {messages:,}\n"
            f"   └─ XP: {xp}\n\n"
        )

    text += "═" * 40 + "\n"

    await update.message.reply_text(text, parse_mode="HTML")
