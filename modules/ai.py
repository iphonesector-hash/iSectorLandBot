import aiohttp
import random
from datetime import datetime

GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """تو Sector AI هستی، دستیار هوشمند و دوستانه گروه تلگرامی SectorLand.

شخصیت تو:
- خودمونی، شوخ‌طبع و صمیمی هستی
- با کاربرا مثل دوست قدیمی حرف میزنی
- از اسم کاربر استفاده میکنی
- جواب‌هات کوتاه و جذابه (حداکثر ۳-۴ جمله)
- از ایموجی استفاده میکنی
- فارسی صحبت میکنی

تخصص‌هات:
- جواب دادن به سوالات روزمره
- قیمت طلا، دلار، ماشین، موبایل (تخمین میزنی و میگی قیمت تقریبیه)
- پیشنهاد غذا و دستور پخت
- فال حافظ و سرگرمی
- بازی و چالش با کاربرا
- خلاصه متن و ترجمه

وقتی کسی سلام میکنه گرم جوابش رو بده.
هیچوقت نگو نمیدونم - یه جواب خلاقانه بده."""


async def ask_groq(user_message: str, user_name: str = "", extra_context: str = "") -> str:
    content = f"نام کاربر: {user_name}\n"
    if extra_context:
        content += f"اطلاعات اضافه: {extra_context}\n"
    content += f"پیام کاربر: {user_message}"

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content}
        ],
        "temperature": 0.9,
        "max_tokens": 300
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
                timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                data = await resp.json()
                if resp.status != 200:
                    error_msg = data.get("error", {}).get("message", "unknown")
                    print(f"Groq error {resp.status}: {error_msg}")
                    return f"🤖 خطا: {error_msg}"
                return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Groq exception: {e}")
        return f"🤖 خطای اتصال: {e}"


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

    is_private = update.effective_chat.type == "private"

    is_reply_to_bot = (
        msg.reply_to_message is not None and
        msg.reply_to_message.from_user is not None and
        msg.reply_to_message.from_user.is_bot
    )

    trigger_words = ["ربات سکتور", "sector ai", "سکتور"]
    is_triggered = any(t in text.lower() for t in trigger_words)

    bot_username = (context.bot.username or "").lower()
    is_mentioned = f"@{bot_username}" in text.lower()

    if not (is_private or is_reply_to_bot or is_triggered or is_mentioned):
        return

    menu_keywords = [
        "سرگرمی", "کاربردی", "مدیریت", "قفل‌ها", "پروفایل",
        "رتبه‌بندی", "تنظیمات", "پشتیبانی", "برگشت", "جوک",
        "فکت", "انگیزشی", "تاس", "چیستان", "اخطار", "بن کن",
        "کیک کن", "میوت", "آنبن", "آنمیوت", "Sector AI",
        "قفل لینک", "قفل فوروارد", "قفل عکس"
    ]
    if text in menu_keywords:
        return

    if "فال" in text:
        await msg.reply_text(get_fal(), parse_mode="HTML")
        return

    await context.bot.send_chat_action(update.effective_chat.id, "typing")

    extra = f"تاریخ: {datetime.now().strftime('%Y-%m-%d')} | ساعت: {datetime.now().strftime('%H:%M')}"
    response = await ask_groq(text, user.first_name, extra)
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
            Commit changes

