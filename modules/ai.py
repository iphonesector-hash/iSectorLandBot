import aiohttp
from collections import defaultdict, deque

# ================= KEYS =================
OPENMODEL_API_KEY = "om-DcBRZP5GbdnxDApshaFpKtJsmrAikr4ik2HdrGXoEhQp"
GROQ_API_KEY = "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"
OPENROUTER_API_KEY = "sk-or-v1-a25674f07c42e7931b5b8e46f034eba7bb2e912c1bc93fa3d2d821cc835b47f"
TAVILY_API_KEY = "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-UEx987lGw4"

# ================= CONFIG =================
OPENMODEL_URL = "https://openmodel.ai/api/v1/chat/completions"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
TAVILY_URL = "https://api.tavily.com/search"

memory = defaultdict(lambda: deque(maxlen=8))

SYSTEM_PROMPT = """
تو Sector AI هستی، دستیار هوشمند SectorLand.
قوانین:
- فارسی روان و خودمونی صحبت کن
- از ایموجی مناسب استفاده کن
- کوتاه ولی باهوش جواب بده
- فقط به صاحب ربات با شناسه مشخص بگو "فرمانده پیمان"
- به بقیه کاربران با احترام جواب بده
"""

MENU_TEXTS = {
    "سرگرمی", "کاربردی", "مدیریت", "قفل‌ها", "پروفایل",
    "رتبه‌بندی", "تنظیمات", "پشتیبانی", "فال حافظ", "جوک",
    "فکت", "انگیزشی", "متن", "تاس", "شیر یا خط", "چیستان",
    "سنگ کاغذ قیچی", "سنگ", "کاغذ", "قیچی", "آب و هوا",
    "ترجمه", "حساب‌گر", "تبدیل واحد", "اخطار", "بن", "آنبن",
    "کیک", "میوت", "آنمیوت", "کیف پول", "جایزه روزانه",
    "حدس کلمه", "حدس پرچم", "دوئل", "دزد و پلیس", "برگشت",
    "سکه و بانک", "واریز به بانک", "برداشت از بانک", "انتقال سکه",
    "وام", "پرداخت وام", "قفل لینک", "قفل عکس", "قفل فیلم",
    "قفل آهنگ", "قفل استیکر", "قفل گیف", "قفل فایل", "قفل فوروارد",
    "قفل متن", "باز کردن همه", "خوش‌آمدگویی", "ضد لینک", "ضد اسپم",
    "زبان", "تنظیم پروفایل", "شخصی‌سازی", "اعلان‌ها", "قوانین",
    "اخطارها", "اخراج", "سکوت", "رفع سکوت", "پیام همگانی",
    "آن‌بن", "پروفایل"
}

SEARCH_WORDS = [
    "قیمت", "طلا", "دلار", "ارز", "خبر", "اخبار",
    "هوا", "آب و هوا", "بیت کوین", "crypto", "بورس"
]


async def search_web(text: str) -> str:
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post(
                TAVILY_URL,
                json={
                    "api_key": TAVILY_API_KEY,
                    "query": text,
                    "max_results": 3,
                    "include_answer": True
                },
                timeout=aiohttp.ClientTimeout(total=10)
            ) as r:
                data = await r.json()
                return data.get("answer", "")
    except Exception:
        return ""


async def call_ai(url: str, key: str, model: str, messages: list) -> str | None:
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.85,
        "max_tokens": 1000
    }
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post(
                url,
                json=payload,
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json"
                },
                timeout=aiohttp.ClientTimeout(total=30)
            ) as r:
                data = await r.json()
                if r.status != 200:
                    return None
                return data["choices"][0]["message"]["content"]
    except Exception:
        return None


async def smart_ai(text: str, name: str, history: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"نام کاربر: {name}\n\nحافظه قبلی:\n{history}\n\nپیام جدید:\n{text}"}
    ]

    for url, key, model in [
        (OPENMODEL_URL, OPENMODEL_API_KEY, "deepseek-v4-flash"),
        (GROQ_URL, GROQ_API_KEY, "llama-3.3-70b-versatile"),
        (OPENROUTER_URL, OPENROUTER_API_KEY, "meta-llama/llama-3.3-70b-instruct:free"),
    ]:
        result = await call_ai(url, key, model, messages)
        if result:
            return result

    return "🤖 الان جواب ندادم، دوباره امتحان کن 😅"


def need_search(text: str) -> bool:
    return any(x in text.lower() for x in SEARCH_WORDS)


async def ai_handler(update, context):
    from config import OWNER_ID

    msg = update.message
    if not msg or not msg.text:
        return

    text = msg.text.strip()

    # اگه متن یه دکمه منوئه رد کن
    cleaned = text
    for emoji in ["🎮","🛠","🛡","🔒","👤","🏆","💰","📖","⚙️","🆘",
                  "😂","🧠","💪","✨","🎲","🪙","🧩","✂️","🌤","🌐",
                  "🔢","📐","🔙","⚠️","📋","👢","🚫","🔓","🔇","🔊",
                  "📢","🔗","🖼","🎬","🎵","🎞","📎","↪️","💬","👋",
                  "🎯","🏳️","⚔️","🚔","👛","🎁","🏦","💸","🤝","📊"]:
        cleaned = cleaned.replace(emoji, "")
    cleaned = cleaned.strip()

    if cleaned in MENU_TEXTS:
        return

    if text.startswith("/"):
        return

    user = update.effective_user
    chat_type = update.effective_chat.type

    if chat_type in ["group", "supergroup"]:
        bot_username = (context.bot.username or "").lower()
        mention = f"@{bot_username}" in text.lower()
        reply_bot = (
            msg.reply_to_message
            and msg.reply_to_message.from_user
            and msg.reply_to_message.from_user.is_bot
        )
        if not mention and not reply_bot:
            return

    name = user.first_name
    if user.id == OWNER_ID:
        name = "فرمانده پیمان"

    await context.bot.send_chat_action(update.effective_chat.id, "typing")

    history = "\n".join(memory[user.id])

    if need_search(text):
        info = await search_web(text)
        if info:
            text += f"\n\nاطلاعات به‌روز از اینترنت:\n{info}"

    answer = await smart_ai(text, name, history)

    memory[user.id].append(f"کاربر: {text[:200]}")
    memory[user.id].append(f"ربات: {answer[:200]}")

    await msg.reply_text(answer)
