import aiohttp
import random
from collections import defaultdict, deque


# ================= KEYS =================

OPENMODEL_API_KEY = "om-DcBRZP5GbdnxDApshaFpKtJsmrAikr4ik2HdrGXoEhQp"

GROQ_API_KEY = "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"

OPENROUTER_API_KEY = "sk-or-v1-a25674f07c42e7931b5b8e46f034eba7bb2e912c1bc93fa3d2d821cc835b47f"

TAVILY_API_KEY = "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-UEx987lGw4"


# ================= CONFIG =================

OWNER_ID = 5147526780

OPENMODEL_URL = "https://openmodel.ai/api/v1/chat/completions"

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

TAVILY_URL = "https://api.tavily.com/search"


memory = defaultdict(lambda: deque(maxlen=5))


SYSTEM_PROMPT = """
تو Sector AI هستی، دستیار هوشمند SectorLand.

قوانین:
- فارسی روان و خودمونی
- ایموجی استفاده کن
- کوتاه ولی باهوش جواب بده
- فقط صاحب ربات را "فرمانده پیمان" صدا کن
- به بقیه کاربران عادی جواب بده
"""


MENU_TEXTS = {
"🎮 سرگرمی","🛠 کاربردی",
"🛡 مدیریت","🔒 قفل‌ها",
"👤 پروفایل","🏆 رتبه‌بندی",
"⚙️ تنظیمات","🆘 پشتیبانی",
"📖 فال حافظ",
"😂 جوک","🧠 فکت",
"💪 انگیزشی","✨ متن",
"🎲 تاس","🪙 شیر یا خط",
"🧩 چیستان","✂️ سنگ کاغذ قیچی",
"سنگ","کاغذ","قیچی",
"🌤 آب و هوا",
"🌐 ترجمه",
"🔢 حساب‌گر",
"📐 تبدیل واحد",
"⚠️ اخطار",
"🚫 بن",
"✅ آنبن",
"👢 کیک",
"🔇 میوت",
"🔊 آنمیوت"
}


SEARCH_WORDS = [
"قیمت","طلا","دلار",
"ارز","خبر","اخبار",
"هوا","آب و هوا"
]


async def search_web(text):

    try:

        async with aiohttp.ClientSession() as s:

            async with s.post(
                TAVILY_URL,
                json={
                    "api_key":TAVILY_API_KEY,
                    "query":text,
                    "max_results":3,
                    "include_answer":True
                },
                timeout=10
            ) as r:

                data = await r.json()

                return data.get(
                    "answer",
                    ""
                )

    except Exception as e:
        print("SEARCH ERROR",e)
        return ""



async def call_ai(
url,
key,
model,
text,
name,
history=""
):

    payload={

        "model":model,

        "messages":[

            {
            "role":"system",
            "content":SYSTEM_PROMPT
            },

            {
            "role":"user",
            "content":f"""

نام:
{name}

حافظه:
{history}

پیام:
{text}

"""
            }

        ],

        "temperature":0.8,
        "max_tokens":700

    }


    async with aiohttp.ClientSession() as s:

        async with s.post(
            url,
            json=payload,
            headers={
                "Authorization":
                f"Bearer {key}",

                "Content-Type":
                "application/json"
            },
            timeout=30

        ) as r:


            data = await r.json()


            if r.status != 200:

                print(
                    "AI ERROR",
                    data
                )

                return None


            return (
            data["choices"][0]
            ["message"]["content"]
            )



async def ask_openmodel(
text,
name,
history
):

    return await call_ai(
        OPENMODEL_URL,
        OPENMODEL_API_KEY,
        "deepseek-v4-flash",
        text,
        name,
        history
    )







async def ask_groq(
text,
name,
history
):

    return await call_ai(
        GROQ_URL,
        GROQ_API_KEY,
        "llama-3.3-70b-versatile",
        text,
        name,
        history
    )



async def ask_openrouter(
text,
name,
history
):

    return await call_ai(
        OPENROUTER_URL,
        OPENROUTER_API_KEY,
        "meta-llama/llama-3.3-70b-instruct:free",
        text,
        name,
        history
    )




async def smart_ai(
text,
name,
history
):

    try:

        result = await ask_openmodel(
            text,
            name,
            history
        )

        if result:
            return result


    except Exception as e:

        print(
            "OPENMODEL FAIL",
            e
        )


    try:

        result = await ask_groq(
            text,
            name,
            history
        )

        if result:
            return result


    except Exception as e:

        print(
            "GROQ FAIL",
            e
        )


    try:

        result = await ask_openrouter(
            text,
            name,
            history
        )

        if result:
            return result


    except Exception as e:

        print(
            "OPENROUTER FAIL",
            e
        )


    return "🤖 الان جواب ندادم 😅"




def need_search(text):

    return any(
        x in text.lower()
        for x in SEARCH_WORDS
    )




async def ai_handler(
update,
context
):


    msg = update.message


    if not msg or not msg.text:
        return


    text = msg.text.strip()


    if text in MENU_TEXTS:
        return


    if text.startswith("/"):
        return



    user = update.effective_user



    if update.effective_chat.type in [
        "group",
        "supergroup"
    ]:


        bot = (
        context.bot.username or ""
        ).lower()


        mention = (
        f"@{bot}" in text.lower()
        )


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



    await context.bot.send_chat_action(
        update.effective_chat.id,
        "typing"
    )



    history = "\n".join(
        memory[user.id]
    )



    if need_search(text):

        info = await search_web(text)

        text += "\n\nاطلاعات جدید:\n" + info



    answer = await smart_ai(
        text,
        name,
        history
    )



    memory[user.id].append(
        "User: " + text
    )

    memory[user.id].append(
        "AI: " + answer
    )



    await msg.reply_text(
        answer
    )





async def ai_ban_reaction(update,context,name):

    await update.message.reply_text(
        f"🚫 {name} بن شد 😅"
    )



async def ai_kick_reaction(update,context,name):

    await update.message.reply_text(
        f"👢 {name} کیک شد"
    )



async def ai_warn_reaction(update,context,name,count,limit):

    await update.message.reply_text(
        f"⚠️ {name} اخطار گرفت"
    )




def get_fal():

    return (
        "🔮 فال امروز:\n\n"
        "✨ روز خوبی برای شروع کارهای جدید است 🌱"
    )
