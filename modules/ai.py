import aiohttp
import random
from datetime import datetime

GROQ_API_KEY = "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"
TAVILY_API_KEY = "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"

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
TAVILY_URL = "https://api.tavily.com/search"

SYSTEM_PROMPT = """تو Sector AI هستی، دستیار باهوش و صمیمی گروه تلگرامی SectorLand.

شخصیت:
- فارسی روون و خودمونی صحبت میکنی
- از ایموجی استفاده میکنی  
- جواب‌هات کوتاه و مفیده (۲-۴ جمله)
- با کاربر دوستانه و شوخ‌طبع هستی

وقتی اطلاعات جستجو بهت داده میشه:
- اطلاعات رو خلاصه و ساده بگو
- منبع رو ذکر نکن
- فارسی توضیح بده
- عدد و رقم دقیق بده"""

MENU_TEXTS = {
    "🎮 سرگرمی", "🛠 کاربردی", "🛡 مدیریت", "🔒 قفل‌ها",
    "👤 پروفایل", "🏆 رتبه‌بندی", "⚙️ تنظیمات", "🆘 پشتیبانی",
    "🤖 Sector AI", "📖 فال حافظ", "🔙 برگشت",
    "😂 جوک", "🧠 فکت", "💪 انگیزشی", "✨ متن",
    "🎲 تاس", "🪙 شیر یا خط", "🧩 چیستان", "✂️ سنگ کاغذ قیچی",
    "🌤 آب و هوا", "🌐 ترجمه", "🔢 حساب‌گر", "📐 تبدیل واحد",
    "⚠️ اخطار", "🧹 پاک اخطار", "📋 اخطارها",
    "🚫 بن", "✅ آنبن", "👢 کیک", "🔇 میوت", "🔊 آنمیوت",
    "⚙️ تنظیم حد اخطار",
    "قفل لینک", "حذف قفل لینک", "قفل فوروارد", "حذف قفل فوروارد",
    "قفل یوزرنیم", "حذف قفل یوزرنیم", "قفل عکس", "حذف قفل عکس",
    "قفل ویدیو", "حذف قفل ویدیو", "قفل فایل", "حذف قفل فایل",
    "قفل استیکر", "حذف قفل استیکر",
    "🟢 ضداسپم روشن کن", "🔴 ضداسپم خاموش کن",
    "🟢 فیلتر لینک روشن کن", "🔴 فیلتر لینک خاموش کن",
    "🟢 فیلتر منشن روشن کن", "🔴 فیلتر منشن خاموش کن",
    "🟢 خوش‌آمدگویی روشن کن", "🔴 خوش‌آمدگویی خاموش کن",
    "✏️ تغییر پیام خوش‌آمد", "📜 قوانین گروه",
    "سنگ", "کاغذ", "قیچی",
}

# کلمات کلیدی که نیاز به جستجو دارن
SEARCH_TRIGGERS = [
    "قیمت", "طلا", "سکه", "دلار", "یورو", "ارز",
    "آب و هوا", "هوا", "دما", "باران", "برف",
    "خبر", "اخبار", "امروز", "جدیدترین",
    "موبایل", "گوشی", "ماشین", "خودرو",
    "بورس", "سهام", "ارز دیجیتال", "بیتکوین",
]


async def search_web(query: str) -> str:
    """جستجو در اینترنت با Tavily"""
    try:
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "basic",
            "max_results": 3,
            "include_answer": True
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                TAVILY_URL,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status != 200:
                    return ""
                data = await resp.json()

                # اگه جواب مستقیم داشت
                if data.get("answer"):
                    return f"[نتیجه جستجو: {data['answer']}]"

                # وگرنه از نتایج استفاده کن
                results = data.get("results", [])
                if not results:
                    return ""

                snippets = []
                for r in results[:2]:
                    content = r.get("content", "")[:200]
                    if content:
                        snippets.append(content)

                return f"[نتایج جستجو: {' | '.join(snippets)}]"
    except Exception as e:
        print(f"Tavily error: {e}")
        return ""


async def ask_groq(user_message: str, user_name: str = "", search_context: str = "") -> str:
    content = f"نام کاربر: {user_name}\n"
    if search_context:
        content += f"اطلاعات از اینترنت: {search_context}\n"
    content += f"پیام کاربر: {user_message}"

    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content}
        ],
        "temperature": 0.7,
        "max_tokens": 400
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                GROQ_URL,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {GROQ_API_KEY}"
                },
                timeout=aiohttp.ClientTimeout(total=20)
            ) as resp:
                data = await resp.json()
                if resp.status != 200:
                    print(f"Groq error: {data}")
                    return "🤖 یه لحظه مشکل داشتم، دوباره بپرس!"
                return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Groq exception: {e}")
        return "🤖 خطای اتصال، دوباره امتحان کن!"


def needs_search(text: str) -> bool:
    """چک میکنه آیا پیام نیاز به جستجو داره"""
    text_lower = text.lower()
    return any(trigger in text_lower for trigger in SEARCH_TRIGGERS)


def build_search_query(text: str) -> str:
    """query جستجو رو میسازه"""
    today = datetime.now().strftime("%Y-%m-%d")
    if any(w in text for w in ["قیمت", "طلا", "سکه", "دلار", "ارز"]):
        return f"قیمت روز {text} {today} ایران"
    if any(w in text for w in ["هوا", "آب و هوا", "دما"]):
        return f"آب و هوا {text} امروز"
    if any(w in text for w in ["خبر", "اخبار"]):
        return f"اخبار امروز ایران {today}"
    return f"{text} {today}"


HAFEZ = [
    "الا یا ایها الساقی ادر کاساً و ناولها\nکه عشق آسان نمود اول ولی افتاد مشکل‌ها\n\n✨ تفسیر: مسیر سختی در پیش داری، ولی پایانش شیرینه.",
    "بیا که قصر امل سخت سست بنیاد است\nبیار باده که بنیاد عمر بر باد است\n\n✨ تفسیر: از لحظه حال لذت ببر، فرصت رو از دست نده.",
    "حافظ اسرار الهی کس نمی‌داند خموش\nاز که می‌پرسی که دور روزگاران را چه شد\n\n✨ تفسیر: صبر کن، جواب سوالت به زودی روشن میشه.",
    "خوشا دلی که مدام از پی نظر نرود\nبه هر درِ که بزد مشتری بدر نرود\n\n✨ تفسیر: روی هدفت تمرکز کن، پراکنده نباش.",
    "شب تاریک و بیم موج و گردابی چنین هائل\nکجا دانند حال ما سبکباران ساحل‌ها\n\n✨ تفسیر: سختی‌های تو رو کسی درک نمیکنه، ولی از پسش برمیای.",
]


def get_fal():
    return f"📖 <b>فال حافظ</b>\n\n{random.choice(HAFEZ)}"


async def ai_handler(update, context):
    msg = update.message
    if not msg or not msg.text:
        return

    user = update.effective_user
    text = msg.text.strip()

    if text in MENU_TEXTS:
        return

    is_private = update.effective_chat.type == "private"
    is_reply_to_bot = (
        msg.reply_to_message is not None and
        msg.reply_to_message.from_user is not None and
        msg.reply_to_message.from_user.is_bot
    )
    trigger_words = ["ربات سکتور", "sector ai"]
    is_triggered = any(t in text.lower() for t in trigger_words)
    bot_username = (context.bot.username or "").lower()
    is_mentioned = f"@{bot_username}" in text.lower()

    if not (is_private or is_reply_to_bot or is_triggered or is_mentioned):
        return

    if "فال" in text:
        await msg.reply_text(get_fal(), parse_mode="HTML")
        return

    await context.bot.send_chat_action(update.effective_chat.id, "typing")

    # جستجو در اینترنت اگه نیاز بود
    search_context = ""
    if needs_search(text):
        await context.bot.send_chat_action(update.effective_chat.id, "typing")
        query = build_search_query(text)
        search_context = await search_web(query)

    response = await ask_groq(text, user.first_name, search_context)
    await msg.reply_text(response)


async def ai_ban_reaction(update, context, banned_user_name: str):
    reactions = [
        f"🚨 {banned_user_name} از گروه پرتاب شد! خداحافظ 👋",
        f"🔨 {banned_user_name} به تاریخ پیوست 😅",
        f"🚫 {banned_user_name} بن شد. قوانین شوخی بردار نیست!",
    ]
    await update.message.reply_text(random.choice(reactions))


async def ai_kick_reaction(update, context, kicked_user_name: str):
    reactions = [
        f"👢 {kicked_user_name} کیک خورد! شاید دفعه دیگه مؤدب‌تر باشه 😄",
        f"🚪 {kicked_user_name} از در رفت بیرون!",
        f"👋 {kicked_user_name} فعلاً برو، شاید بعداً برگردی!",
    ]
    await update.message.reply_text(random.choice(reactions))


async def ai_warn_reaction(update, context, warned_user_name: str, count: int, limit: int):
    if count >= limit - 1:
        await update.message.reply_text(
            f"⚠️ {warned_user_name} یه قدم تا بن فاصله داری! مراقب باش 😬"
        )
    else:
        reactions = [
            f"🤨 {warned_user_name}، داری اشتباه میری!",
            f"😤 {warned_user_name} اخطار گرفت. ادامه بده ببین چی میشه!",
        ]
        await update.message.reply_text(random.choice(reactions))
