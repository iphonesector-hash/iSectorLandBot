import aiohttp
import json
import random
from datetime import datetime

GEMINI_API_KEY = "AIzaSyAb8RN6JpVL0K5dXd6OeNztiuqZCYSUCCpOlPmXlXYBHCfORRnQ"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

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
وقتی کسی بن یا کیک میشه یه پیام طنزآمیز بنویس.
هیچوقت نگو نمیدونم — یه جواب خلاقانه بده."""


async def ask_gemini(user_message: str, user_name: str = "", extra_context: str = "") -> str:
    prompt = f"نام کاربر: {user_name}\n"
    if extra_context:
        prompt += f"اطلاعات اضافه: {extra_context}\n"
    prompt += f"پیام کاربر: {user_message}"

    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.9,
            "maxOutputTokens": 300
        }
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{GEMINI_URL}?key={GEMINI_API_KEY}",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                if resp.status != 200:
                    return "🤖 الان یکم سرم شلوغه، بعداً بپرس!"
                data = await resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return "🤖 یه مشکل کوچیک پیش اومد، دوباره امتحان کن!"


# ─── فال حافظ ───────────────────────────────────────────
HAFEZ = [
    "الا یا ایها الساقی ادر کاساً و ناولها\nکه عشق آسان نمود اول ولی افتاد مشکل‌ها\n\n✨ تفسیر: مسیر سختی در پیش داری، ولی پایانش شیرینه.",
    "بیا که قصر امل سخت سست بنیاد است\nبیار باده که بنیاد عمر بر باد است\n\n✨ تفسیر: از لحظه حال لذت ببر، فرصت رو از دست نده.",
    "حافظ اسرار الهی کس نمی‌داند خموش\nاز که می‌پرسی که دور روزگاران را چه شد\n\n✨ تفسیر: صبر کن، جواب سوالت به زودی روشن میشه.",
    "خوشا دلی که مدام از پی نظر نرود\nبه هر درِ که بزد مشتری بدر نرود\n\n✨ تفسیر: روی هدفت تمرکز کن، پراکنده نباش.",
    "شب تاریک و بیم موج و گردابی چنین هائل\nکجا دانند حال ما سبکباران ساحل‌ها\n\n✨ تفسیر: سختی‌های تو رو کسی درک نمیکنه، ولی از پسش برمیای.",
]


def get_fal():
    return f"📖 <b>فال حافظ</b>\n\n{random.choice(HAFEZ)}"


# ─── هندلر اصلی AI ──────────────────────────────────────
async def ai_handler(update, context):
    msg = update.message
    user = update.effective_user
    text = msg.text or ""

    is_private = update.effective_chat.type == "private"

    is_reply_to_bot = (
        msg.reply_to_message is not None and
        msg.reply_to_message.from_user is not None and
        msg.reply_to_message.from_user.is_bot
    )

    bot_username = context.bot.username or ""
    trigger_words = ["ربات سکتور", "سکتور", f"@{bot_username}"]
    is_mentioned = any(t.lower() in text.lower() for t in trigger_words)

    if not (is_private or is_reply_to_bot or is_mentioned):
        return

    # پیام‌های منو رو رد کن
    menu_keywords = [
        "سرگرمی", "کاربردی", "مدیریت", "قفل", "پروفایل",
        "رتبه", "تنظیمات", "پشتیبانی", "برگشت", "جوک",
        "فکت", "انگیزشی", "تاس", "چیستان", "اخطار", "بن",
        "کیک", "میوت", "آنبن", "آنمیوت", "Sector AI"
    ]
    if any(k in text for k in menu_keywords):
        return

    # فال حافظ
    if "فال" in text:
        await msg.reply_text(get_fal(), parse_mode="HTML")
        return

    # نشانه تایپ
    await context.bot.send_chat_action(update.effective_chat.id, "typing")

    # اطلاعات اضافه برای context
    extra = f"تاریخ امروز: {datetime.now().strftime('%Y-%m-%d')} | ساعت: {datetime.now().strftime('%H:%M')}"

    response = await ask_gemini(text, user.first_name, extra)
    await msg.reply_text(response)


# ─── واکنش به دستورات مدیریتی ───────────────────────────
async def ai_ban_reaction(update, context, banned_user_name: str):
    reactions = [
        f"🚨 {banned_user_name} از گروه پرتاب شد! خداحافظ 👋",
        f"🔨 یه نفر دیگه رفت! {banned_user_name} به تاریخ پیوست 😅",
        f"🚫 {banned_user_name} بن شد. قوانین گروه شوخی بردار نیست!",
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
            f"⚠️ {warned_user_name} یه قدم تا بن فاصله داری! بهتره مراقب باشی 😬"
        )
    else:
        reactions = [
            f"🤨 {warned_user_name}، داری اشتباه میری ها!",
            f"😤 {warned_user_name} اخطار گرفت. ادامه بده ببین چی میشه!",
        ]
        await update.message.reply_text(random.choice(reactions))
