import aiohttp
from collections import defaultdict, deque


# ================= KEYS =================

OPENMODEL_API_KEY = "om-DcBRZP5GbdnxDApshaFpKtJsmrAikr4ik2HdrGXoEhQp"
GROQ_API_KEY = "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"
OPENROUTER_API_KEY = "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"
TAVILY_API_KEY = "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-UEx987lGw4"


# ================= URLS =================

OPENMODEL_URL = "https://openmodel.ai/api/v1/chat/completions"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
TAVILY_URL = "https://api.tavily.com/search"


# ================= MEMORY =================

memory = defaultdict(lambda: deque(maxlen=8))


SYSTEM_PROMPT = """
تو Sector AI هستی، دستیار هوشمند SectorLand.

قوانین:
- فارسی روان و خودمونی صحبت کن
- کوتاه و مفید جواب بده
- ایموجی مناسب استفاده کن
- اگر کاربر صاحب ربات بود او را فرمانده پیمان صدا کن
"""


# ================= API =================


async def call_ai(url, key, model, messages):

    if not key or key.startswith("PUT"):
        return None

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 800
    }

    try:

        timeout = aiohttp.ClientTimeout(total=30)

        async with aiohttp.ClientSession(timeout=timeout) as session:

            async with session.post(
                url,
                json=payload,
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json"
                }
            ) as response:


                if response.status != 200:
                    print(
                        "AI ERROR:",
                        response.status,
                        await response.text()
                    )
                    return None


                data = await response.json()

                return data["choices"][0]["message"]["content"]


    except Exception as e:

        print("AI REQUEST ERROR:", e)
        return None



# ================= SMART AI =================


async def smart_ai(text, name="کاربر", history=""):


    messages = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },

        {
            "role": "user",
            "content": f"""
نام کاربر:
{name}

حافظه:
{history}

پیام:
{text}
"""
        }

    ]


    providers = [

        (
            OPENROUTER_URL,
            OPENROUTER_API_KEY,
            "meta-llama/llama-3.3-70b-instruct:free"
        ),

        (
            GROQ_URL,
            GROQ_API_KEY,
            "llama-3.3-70b-versatile"
        ),

        (
            OPENMODEL_URL,
            OPENMODEL_API_KEY,
            "deepseek-chat"
        )

    ]


    for url, key, model in providers:

        result = await call_ai(
            url,
            key,
            model,
            messages
        )

        if result:
            return result



    return "🤖 هوش مصنوعی فعلاً جواب نداد 😅"



# ================= SEARCH =================


async def search_web(text):

    if not TAVILY_API_KEY or TAVILY_API_KEY.startswith("PUT"):
        return ""


    try:

        async with aiohttp.ClientSession() as session:

            async with session.post(

                TAVILY_URL,

                json={
                    "api_key": TAVILY_API_KEY,
                    "query": text,
                    "max_results": 3,
                    "include_answer": True
                }

            ) as r:

                data = await r.json()

                return data.get("answer","")


    except Exception as e:

        print("SEARCH ERROR:",e)
        return ""



def need_search(text):

    words = [
        "قیمت",
        "طلا",
        "دلار",
        "خبر",
        "اخبار",
        "هوا",
        "آب و هوا",
        "بیت کوین",
        "ارز"
    ]


    return any(
        x in text.lower()
        for x in words
    )



# ================= TELEGRAM AI =================


async def ai_handler(update, context):

    from config import OWNER_ID


    msg = update.message


    if not msg or not msg.text:
        return


    text = msg.text.strip()


    if text.startswith("/"):
        return



    user = update.effective_user

    name = (
        "فرمانده پیمان"
        if user.id == OWNER_ID
        else user.first_name
    )


    await context.bot.send_chat_action(
        update.effective_chat.id,
        "typing"
    )



    history = "\n".join(
        memory[user.id]
    )



    if need_search(text):

        info = await search_web(text)

        if info:

            text += (
                "\n\nاطلاعات به‌روز:\n"
                + info
            )



    answer = await smart_ai(
        text,
        name,
        history
    )


    memory[user.id].append(
        "کاربر: " + text[:150]
    )

    memory[user.id].append(
        "ربات: " + answer[:150]
    )


    await msg.reply_text(answer)



# ================= HAFEZ =================


async def get_fal(update, context):

    result = await smart_ai(
        """
یک فال حافظ بگیر.
یک بیت از حافظ بده.
بعد تعبیر کوتاه و مثبت بنویس.
""",
        "کاربر"
    )


    await update.message.reply_text(
        "📖 فال حافظ\n\n" + result
    )
