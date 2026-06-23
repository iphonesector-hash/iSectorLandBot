import aiohttp
import random


GROQ_API_KEY = "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"

OPENROUTER_API_KEY = "sk-or-v1-a25674f07c42e7931b5b8e46f034eba7bb2e912c1bc93fa3d2d821cc835b47f"

TAVILY_API_KEY = "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-UEx987lGw4"


GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

TAVILY_URL = "https://api.tavily.com/search"



SYSTEM_PROMPT = """
تو Sector AI هستی، دستیار هوشمند SectorLand.

فارسی روان و خودمونی حرف بزن.
ایموجی استفاده کن.
کوتاه و مفید جواب بده.
دوستانه و باحال باش.
"""



MENU_TEXTS = {
"🎮 سرگرمی","🛠 کاربردی","🛡 مدیریت","🔒 قفل‌ها",
"👤 پروفایل","🏆 رتبه‌بندی","⚙️ تنظیمات",
"🆘 پشتیبانی","📖 فال حافظ",
"😂 جوک","🧠 فکت","💪 انگیزشی",
"✨ متن","🎲 تاس","🪙 شیر یا خط",
"🧩 چیستان","✂️ سنگ کاغذ قیچی",
"سنگ","کاغذ","قیچی",
"🌤 آب و هوا","🌐 ترجمه",
"🔢 حساب‌گر","📐 تبدیل واحد",
"⚠️ اخطار","🚫 بن",
"✅ آنبن","👢 کیک",
"🔇 میوت","🔊 آنمیوت"
}



SEARCH = [
"قیمت","طلا","دلار",
"ارز","خبر","اخبار",
"هوا","آب و هوا"
]



async def search_web(text):

    try:

        async with aiohttp.ClientSession() as s:

            r = await s.post(
                TAVILY_URL,
                json={
                    "api_key":TAVILY_API_KEY,
                    "query":text,
                    "max_results":3,
                    "include_answer":True
                },
                timeout=10
            )

            data = await r.json()

            return data.get("answer","")

    except Exception as e:

        print("TAVILY:",e)
        return ""





async def ask_ai(
    url,
    key,
    model,
    text,
    name,
    search=""
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

اطلاعات:
{search}

پیام:
{text}
"""
            }

        ],

        "temperature":0.7,
        "max_tokens":500
    }



    try:

        async with aiohttp.ClientSession() as s:

            r = await s.post(
                url,
                json=payload,
                headers={
                    "Authorization":f"Bearer {key}",
                    "Content-Type":"application/json"
                },
                timeout=30
            )


            data = await r.json()


            if r.status != 200:

                print("AI ERROR:",data)
                return None



            return data["choices"][0]["message"]["content"]


    except Exception as e:

        print("AI EXCEPTION:",e)
        return None





async def ask_groq(
    text,
    name,
    search=""
):

    return await ask_ai(
        GROQ_URL,
        GROQ_API_KEY,
        "llama-3.3-70b-versatile",
        text,
        name,
        search
    )





async def ask_openrouter(
    text,
    name,
    search=""
):

    return await ask_ai(
        OPENROUTER_URL,
        OPENROUTER_API_KEY,
        "meta-llama/llama-3.3-70b-instruct:free",
        text,
        name,
        search
    )




def need_search(text):

    return any(
        x in text.lower()
        for x in SEARCH
    )





async def ai_handler(update,context):


    msg = update.message


    if not msg or not msg.text:
        return



    text = msg.text.strip()



    if text.startswith("/"):
        return



    if text in MENU_TEXTS:
        return



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



    answer = await ask_groq(
        text,
        user.first_name,
        search
    )



    if not answer:

        answer = await ask_openrouter(
            text,
            user.first_name,
            search
        )



    if not answer:

        answer="🤖 الان هوش مصنوعی در دسترس نیست"



    await msg.reply_text(answer)






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
    "🔮 فال امروز:\n"
    "✨ روز خوبی برای شروع کارهای جدید است 🌱"
    )
