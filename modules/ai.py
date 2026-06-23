import aiohttp
import random


# ================= KEYS =================

GROQ_API_KEY = "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"

OPENROUTER_API_KEY = "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"

TAVILY_API_KEY = "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"


# ================= URL =================

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

TAVILY_URL = "https://api.tavily.com/search"



SYSTEM_PROMPT = """
تو Sector AI هستی، دستیار هوشمند SectorLand.

- فارسی روان و خودمونی حرف بزن
- ایموجی استفاده کن
- جواب کوتاه و مفید بده
- دوستانه و باحال باش
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



SEARCH = [
"قیمت","طلا","دلار",
"ارز","خبر","اخبار",
"هوا","آب و هوا"
]



async def search_web(text):

    try:

        payload={
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

                data=await r.json()

                return data.get(
                    "answer",
                    ""
                )

    except Exception as e:
        print("Tavily:",e)
        return ""




async def ask_openai_style(
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

            async with s.post(
                url,
                json=payload,
                headers={
                "Authorization":
                f"Bearer {key}",
                "Content-Type":
                "application/json"
                },
                timeout=25
            ) as r:


                data=await r.json()


                if r.status != 200:
                    print("AI ERROR:",data)
                    return None


                return data["choices"][0]["message"]["content"]


    except Exception as e:

        print("AI EXCEPTION:",e)
        return None
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



# ==========================
# OpenRouter AI (Backup AI)
# ==========================

OPENROUTER_API_KEY = "اینجا_کلید_OpenRouter"

OPENROUTER_URL = (
    "https://openrouter.ai/api/v1/chat/completions"
)



async def ask_openrouter(
    user_message,
    user_name="",
    search_context=""
):

    payload = {

        "model": "meta-llama/llama-3.3-70b-instruct:free",

        "messages": [

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": f"""
نام:
{user_name}

اطلاعات:
{search_context}

پیام:
{user_message}
"""
            }
        ],

        "temperature": 0.7,
        "max_tokens": 500
    }


    try:

        async with aiohttp.ClientSession() as session:

            async with session.post(

                OPENROUTER_URL,

                json=payload,

                headers={

                    "Authorization":
                    f"Bearer {OPENROUTER_API_KEY}",

                    "Content-Type":
                    "application/json"

                },

                timeout=30

            ) as resp:


                data = await resp.json()


                if resp.status != 200:

                    print(
                        "OpenRouter Error:",
                        data
                    )

                    return (
                        "🤖 الان هوش مصنوعی "
                        "در دسترس نیست"
                    )


                return (
                    data["choices"][0]
                    ["message"]["content"]
                )


    except Exception as e:

        print(
            "OpenRouter Exception:",
            e
        )

        return "🤖 خطای اتصال"



# جایگزین هندلر اصلی AI
# اول Groq امتحان میشه
# اگر خراب بود OpenRouter

async def smart_ai(
    text,
    name,
    search=""
):

    try:

        result = await ask_groq(
            text,
            name,
            search
        )

        if (
            result and
            "خطای اتصال" not in result and
            "مشکل موقت" not in result
        ):
            return result


    except Exception as e:

        print(
            "Groq failed:",
            e
        )


    return await ask_openrouter(
        text,
        name,
        search
    )



# ==========================
# Test / Profile
# ==========================


def get_fal():

    return (
        "🔮 فال امروز شما:\n\n"
        "✨ امروز زمان خوبی برای شروع "
        "کارهای جدید است.\n"
        "به خودت اعتماد کن 🌱"
    )
