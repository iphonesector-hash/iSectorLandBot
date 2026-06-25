import random
from modules.ai import smart_ai


async def generate_fun(kind: str) -> str:
    prompts = {
        "joke": (
            "یک جوک فارسی کاملاً جدید و خنده‌دار بساز. "
            "کوتاه، خودمونی و با ایموجی باشه. "
            "حتماً جوک جدید و متفاوت باشه."
        ),
        "fact": (
            "یک فکت جالب، عجیب و واقعی فارسی بگو. "
            "کوتاه، با ایموجی و تکراری نباشه. "
            "از اینترنت و دانش به‌روز استفاده کن."
        ),
        "motive": (
            "یک جمله انگیزشی قوی، تازه و تاثیرگذار فارسی بنویس. "
            "با ایموجی و از ته دل باشه."
        ),
        "text": (
            "یک متن کوتاه زیبا، احساسی یا ادبی فارسی بنویس. "
            "با ایموجی و شاعرانه باشه."
        ),
        "riddle": (
            "یک چیستان جدید و جالب فارسی بساز.\n"
            "دقیقاً این فرمت رو رعایت کن:\n"
            "🧩 چیستان:\n"
            "[سوال چیستان اینجا]\n\n"
            "برای دیدن جواب روی دکمه زیر بزن 👇\n"
            "||جواب: [جواب اینجا]||"
        ),
        "fal": (
            "یک فال حافظ کامل و حرفه‌ای فارسی بساز.\n\n"
            "دقیقاً این فرمت رو رعایت کن:\n\n"
            "🔮 فال حافظ\n\n"
            "📜 غزل:\n"
            "[یک بیت یا دوبیت از اشعار واقعی حافظ]\n\n"
            "📖 معنی شعر:\n"
            "[معنی ساده و فارسی روان شعر]\n\n"
            "✨ تفسیر و تعبیر:\n"
            "[تفسیر کامل فال برای زندگی کاربر]\n\n"
            "🌱 پیام امروز:\n"
            "[یک پیام مثبت و امیدوارکننده]\n\n"
            "واقعی، زیبا و الهام‌بخش بنویس."
        ),
    }

    prompt = prompts.get(kind, "یک متن جذاب فارسی بساز")
    try:
        result = await smart_ai(prompt, "کاربر", "")
        return result
    except Exception:
        return "🤖 فعلاً ذهنم قفل کرد 😅 دوباره امتحان کن."


async def get_joke() -> str:
    return await generate_fun("joke")

async def get_fact() -> str:
    return await generate_fun("fact")

async def get_motive() -> str:
    return await generate_fun("motive")

async def get_text() -> str:
    return await generate_fun("text")

async def get_riddle() -> str:
    return await generate_fun("riddle")

async def get_fal() -> str:
    return await generate_fun("fal")


def dice() -> str:
    n = random.randint(1, 6)
    faces = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}
    return f"🎲 عدد تاس: {faces[n]} ({n})"


def coin() -> str:
    result = random.choice(["شیر 🦁", "خط ✍️"])
    return f"🪙 نتیجه: {result}"


def rps(choice: str) -> str:
    options = ["سنگ", "کاغذ", "قیچی"]
    emojis = {"سنگ": "🪨", "کاغذ": "📄", "قیچی": "✂️"}
    win_against = {"سنگ": "قیچی", "کاغذ": "سنگ", "قیچی": "کاغذ"}

    user_key = None
    for o in options:
        if o in choice:
            user_key = o
            break

    if not user_key:
        return "❌ بنویس: سنگ، کاغذ یا قیچی"

    bot_key = random.choice(options)

    if user_key == bot_key:
        result = "🤝 مساوی شد!"
    elif win_against[user_key] == bot_key:
        result = "🎉 تو بردی!"
    else:
        result = "😅 تو باختی!"

    return (
        f"تو: {user_key} {emojis[user_key]}\n"
        f"من: {bot_key} {emojis[bot_key]}\n\n"
        f"{result}"
    )
