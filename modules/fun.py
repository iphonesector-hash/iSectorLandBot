import random


jokes = [
    "😂 چرا کامپیوتر رفت دکتر؟ چون ویروس گرفته بود!",
    "🤣 وای فای قطع شد، مودم رفت استراحت!",
    "😄 برنامه نویس بدون باگ مثل چای بدون قنده!"
]


facts = [
    "🧠 اختاپوس ۳ قلب دارد.",
    "🌎 نور خورشید حدود ۸ دقیقه طول می‌کشد به زمین برسد.",
    "🐬 دلفین‌ها با هم ارتباط مخصوص دارند."
]


motives = [
    "💪 امروز می‌تونه شروع یه اتفاق خوب باشه.",
    "🔥 موفقیت از قدم‌های کوچیک ساخته میشه.",
    "✨ ادامه بده، نزدیک‌تر از چیزی هستی که فکر می‌کنی."
]


texts = [
    "✨ یه روز عالی منتظرته",
    "🌻 انرژی خوب پخش کن",
    "🔥 قوی‌تر از دیروزی"
]


def get_joke():
    return random.choice(jokes)


def get_fact():
    return random.choice(facts)


def get_motive():
    return random.choice(motives)


def get_text():
    return random.choice(texts)


def dice():
    return f"🎲 عدد تاس: {random.randint(1,6)}"


def coin():
    return random.choice(
        ["🪙 شیر", "🪙 خط"]
    )


def riddle():
    return (
        "🧠 چیستان:\n\n"
        "چی دندون داره ولی غذا نمیخوره؟\n\n"
        "جواب: شانه 😄"
    )
