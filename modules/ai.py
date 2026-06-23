import aiohttp
import random


# ================= KEYS =================

GEMINI_API_KEY = "AQ.Ab8RN6LQhGJDV7hOBi2dh6BXksQxLxJc-drfZfiZdKYnna9_rKg"

DEEPSEEK_API_KEY = "sk-0faf5666a01646cab6961f8fb5301568"

GROQ_API_KEY = "gsk_ivhp9RULN9ktGQlN4YOEWGdyb3FY9b-ZT47MQZqHnJAdb6K1T0od9"

TAVILY_API_KEY = " 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-UEx987lGw4"


# ================= URL =================

GEMINI_URL = (
"https://generativelanguage.googleapis.com/v1beta/models/"
"gemini-2.5-flash:generateContent"
)

DEEPSEEK_URL = (
"https://api.deepseek.com/chat/completions"
)

GROQ_URL = (
"https://api.groq.com/openai/v1/chat/completions"
)

TAVILY_URL = (
"https://api.tavily.com/search"
)



SYSTEM_PROMPT = """
تو Sector AI هستی، دستیار هوشمند SectorLand.

- فارسی روان و خودمونی حرف بزن
- ایموجی استفاده کن
- کوتاه و مفید جواب بده
- دوستانه باش
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
"🔊 آنمیوت",

"👛 کیف پول",
"🎁 جایزه روزانه",
"🏦 واریز",
"💸 برداشت"

}



SEARCH = [
"قیمت","طلا","دلار",
"ارز","خبر","اخبار",
"هوا","آب و هوا"
]



async def search_web(text):

    try:

        payload = {

        "api_key":TAVILY_API_KEY,
        "query":text,
        "max_results":3,
        "include_answer":True

        }


        async with aiohttp.ClientSession() as s:

            async with s.post(
                TAVILY_URL,
                json=payload,
                timeout=10
            ) as r:

                data = await r.json()

                return data.get(
                    "answer",
                    ""
                )


    except:

        return ""





async def ask_openai_style(
    url,
    key,
    model,
    text,
    name,
    search=""
):


    payload = {

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

اطلاعات:
{search}

پیام:
{text}
"""
    }

    ],

    "temperature":0.7

    }



    async with aiohttp.ClientSession() as s:

        async with s.post(
            url,
            json=payload,
            headers={
            "Authorization":f"Bearer {key}",
            "Content-Type":"application/json"
            },
            timeout=20
        ) as r:


            data = await r.json()


            if r.status != 200:

                raise Exception()


            return data["choices"][0]["message"]["content"]





async def ask_gemini(
text,
name,
search=""
):

    payload={

    "contents":[
        {
        "parts":[
            {
            "text":f"""
{SYSTEM_PROMPT}

نام:
{name}

{search}

پیام:
{text}
"""
            }
        ]
        }
    ]

    }


    async with aiohttp.ClientSession() as s:

        async with s.post(
        GEMINI_URL +
        f"?key={GEMINI_API_KEY}",
        json=payload,
        timeout=20
        ) as r:


            data=await r.json()


            if r.status != 200:
                raise Exception()


            return (
            data["candidates"][0]
            ["content"]["parts"][0]["text"]
            )





async def ask_deepseek(
text,
name,
search=""
):

    return await ask_openai_style(
    DEEPSEEK_URL,
    DEEPSEEK_API_KEY,
    "deepseek-chat",
    text,
    name,
    search
    )





async def ask_groq(
text,
name,
search=""
):

    return await ask_openai_style(
    GROQ_URL,
    GROQ_API_KEY,
    "llama-3.3-70b-versatile",
    text,
    name,
    search
    )





def need_search(text):

    return any(
    x in text.lower()
    for x in SEARCH
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



    # گروه فقط با صدا زدن

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


        reply = (
        msg.reply_to_message
        and msg.reply_to_message.from_user
        and msg.reply_to_message.from_user.is_bot
        )


        if not mention and not reply:
            return




    user = update.effective_user



    await context.bot.send_chat_action(
    update.effective_chat.id,
    "typing"
    )



    search=""



    if need_search(text):

        search = await search_web(text)



    try:

        answer = await ask_gemini(
        text,
        user.first_name,
        search
        )


    except:

        try:

            answer = await ask_deepseek(
            text,
            user.first_name,
            search
            )


        except:

            answer = await ask_groq(
            text,
            user.first_name,
            search
            )



    await msg.reply_text(answer)





async def ai_ban_reaction(update, context, name):

    await update.message.reply_text(
        f"🚫 {name} بن شد 😅"
    )


async def ai_kick_reaction(update, context, name):

    await update.message.reply_text(
        f"👢 {name} کیک شد"
    )


async def ai_warn_reaction(update, context, name, count, limit):

    await update.message.reply_text(
        f"⚠️ {name} اخطار گرفت"
    )


def get_fal():
    return "🔮 فال امروز شما:\nامروز روز خوبی برای شروع کارهای جدید است ✨"
