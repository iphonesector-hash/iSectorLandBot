import aiohttp
import random
from datetime import datetime

GROQ_API_KEY = "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"
TAVILY_API_KEY = "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"

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
TAVILY_URL = "https://api.tavily.com/search"

SYSTEM_PROMPT = """
تو Sector AI هستی، دستیار باهوش و صمیمی گروه تلگرامی SectorLand.

- فارسی روون و خودمونی صحبت کن
- ایموجی استفاده کن
- جواب‌ها کوتاه و مفید باشن
- دوستانه و شوخ‌طبع باش
"""


MENU_TEXTS = {
    "🎮 سرگرمی", "🛠 کاربردی", "🛡 مدیریت", "🔒 قفل‌ها",
    "👤 پروفایل", "🏆 رتبه‌بندی", "⚙️ تنظیمات",
    "🆘 پشتیبانی", "📖 فال حافظ",
    "😂 جوک", "🧠 فکت", "💪 انگیزشی",
    "✨ متن", "🎲 تاس", "🪙 شیر یا خط",
    "🧩 چیستان", "✂️ سنگ کاغذ قیچی",
    "سنگ", "کاغذ", "قیچی",
    "🌤 آب و هوا", "🌐 ترجمه",
    "🔢 حساب‌گر", "📐 تبدیل واحد",
    "⚠️ اخطار", "🚫 بن",
    "✅ آنبن", "👢 کیک",
    "🔇 میوت", "🔊 آنمیوت",
    "👛 کیف پول", "🎁 جایزه روزانه",
    "🏦 واریز", "💸 برداشت",
}


SEARCH_TRIGGERS = [
    "قیمت", "طلا", "سکه",
    "دلار", "ارز",
    "هوا", "خبر",
    "اخبار"
]


async def search_web(query):

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
                timeout=10
            ) as resp:

                data = await resp.json()

                if data.get("answer"):
                    return data["answer"]

                return ""

    except Exception as e:
        print("Tavily error:", e)
        return ""



async def ask_groq(
    user_message,
    user_name="",
    search_context=""
):

    content = f"""
نام کاربر: {user_name}

{search_context}

پیام:
{user_message}
"""


    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": content
            }
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
                    "Authorization":
                    f"Bearer {GROQ_API_KEY}",
                    "Content-Type":
                    "application/json"
                },
                timeout=20
            ) as resp:


                data = await resp.json()


                if resp.status != 200:
                    print("Groq error:", data)
                    return "🤖 مشکل موقت دارم، دوباره بفرست"


                return data["choices"][0]["message"]["content"]


    except Exception as e:
        print("Groq exception:", e)
        return "🤖 خطای اتصال"



def needs_search(text):

    return any(
        x in text.lower()
        for x in SEARCH_TRIGGERS
    )



HAFEZ = [
    "✨ امروز بهت خوش میگذره، صبور باش.",
    "🌱 مسیرت سختی داره ولی موفق میشی.",
    "⭐ خبرهای خوب نزدیکه."
]


def get_fal():

    return (
        "📖 فال حافظ\n\n"
        + random.choice(HAFEZ)
    )



async def ai_handler(update, context):

    msg = update.message

    if not msg or not msg.text:
        return


    text = # دکمه‌های ربات و منوها را AI جواب ندهد
if text in MENU_TEXTS or any(x in text for x in [
    "🎮", "🛠", "🛡", "🔒",
    "👤", "🏆", "⚙️", "🆘",
    "📖", "😂", "🧠",
    "💪", "✨", "🎲",
    "🪙", "🧩", "✂️",
    "🌤", "🌐", "🔢",
    "📐", "⚠️",
    "🚫", "✅", "👢",
    "🔇", "🔊",
    "👛", "🎁",
    "🏦", "💸"
]):
    return


    user = update.effective_user


    await context.bot.send_chat_action(
        update.effective_chat.id,
        "typing"
    )


    search_context = ""


    if needs_search(text):

        search_context = await search_web(text)



    answer = await ask_groq(
        text,
        user.first_name,
        search_context
    )


    await msg.reply_text(answer)



async def ai_ban_reaction(
    update,
    context,
    banned_user_name
):

    await update.message.reply_text(
        f"🚫 {banned_user_name} بن شد 😅"
    )



async def ai_kick_reaction(
    update,
    context,
    kicked_user_name
):

    await update.message.reply_text(
        f"👢 {kicked_user_name} کیک شد"
    )



async def ai_warn_reaction(
    update,
    context,
    warned_user_name,
    count,
    limit
):

    await update.message.reply_text(
        f"⚠️ {warned_user_name} اخطار گرفت"
    )
