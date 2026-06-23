import random


# ==========================
# AI GENERATED FUN SYSTEM
# ==========================


async def generate_fun(ai_func, kind):

    prompts = {

        "joke":
        """
یک جوک فارسی جدید بساز.
کوتاه، خنده دار، خودمونی و با ایموجی.
هیچ جوکی که قبلا گفتی تکرار نکن.
""",


        "fact":
        """
یک فکت جالب و واقعی فارسی بگو.
کوتاه، عجیب و با ایموجی.
تکراری نباشه.
""",


        "motive":
        """
یک جمله انگیزشی قوی و جدید فارسی بنویس.
کوتاه و تاثیرگذار با ایموجی.
""",


        "text":
        """
یک متن کوتاه زیبا و احساسی فارسی بنویس.
با ایموجی.
""",


        "riddle":
        """
یک چیستان جدید فارسی بساز.
اول سوال را بنویس.
جواب را آخر داخل ||جواب: ...|| قرار بده.
""",


        "fal":
        """
یک فال حافظ حرفه‌ای بساز.

فرمت:
🔮 فال حافظ

📜 شعر حافظ:
(یک بیت یا غزل کوتاه)

✨ تعبیر:
(تفسیر کامل)

🌱 پیام امروز:
(نتیجه مثبت)

واقعی و زیبا بنویس.
"""
    }


    prompt = prompts.get(
        kind,
        "یک متن جذاب فارسی بساز"
    )


    try:

        result = await ai_func(
            prompt,
            "کاربر",
            ""
        )

        return result


    except Exception:

        return "🤖 فعلا ذهنم قفل کرد 😅"



# ==========================
# PUBLIC FUNCTIONS
# ==========================


async def get_joke(ai):

    return await generate_fun(
        ai,
        "joke"
    )



async def get_fact(ai):

    return await generate_fun(
        ai,
        "fact"
    )



async def get_motive(ai):

    return await generate_fun(
        ai,
        "motive"
    )



async def get_text(ai):

    return await generate_fun(
        ai,
        "text"
    )



async def get_riddle(ai):

    return await generate_fun(
        ai,
        "riddle"
    )



async def get_fal(ai):

    return await generate_fun(
        ai,
        "fal"
    )



# ==========================
# OTHER GAMES
# ==========================


def dice():

    n = random.randint(1,6)

    faces = {
        1:"⚀",
        2:"⚁",
        3:"⚂",
        4:"⚃",
        5:"⚄",
        6:"⚅"
    }

    return f"🎲 عدد تاس: {faces[n]} ({n})"



def coin():

    return (
        "🪙 نتیجه: "
        +
        random.choice(
            [
                "شیر 🦁",
                "خط ✍️"
            ]
        )
    )



def rps(choice):

    options = [
        "سنگ 🪨",
        "کاغذ 📄",
        "قیچی ✂️"
    ]


    bot = random.choice(options)


    win = {
        "سنگ":"قیچی",
        "کاغذ":"سنگ",
        "قیچی":"کاغذ"
    }


    user = None

    for x in win:

        if x in choice:
            user=x


    if not user:
        return "❌ بنویس: سنگ، کاغذ یا قیچی"



    bot_key = bot.split()[0]


    if user == bot_key:

        result="🤝 مساوی شد"

    elif win[user] == bot_key:

        result="🎉 بردی"

    else:

        result="😅 باختی"


    return f"""
تو: {choice}
من: {bot}

{result}
"""



def random_number(
    min_val=1,
    max_val=100
):

    return (
        f"🔢 عدد شانسی: "
        f"{random.randint(min_val,max_val)}"
    )
