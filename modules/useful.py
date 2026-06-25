import re
import aiohttp

UNIT_HELP = (
    "📐 <b>تبدیل واحد</b>\n\n"
    "فرمت: <code>/convert مقدار واحد به واحد</code>\n\n"
    "<b>طول:</b> km↔m, m↔cm, cm↔mm, mile↔km, ft↔m\n"
    "<b>وزن:</b> kg↔g, lb↔kg\n"
    "<b>دما:</b> c↔f, c↔k\n\n"
    "مثال: <code>/convert 100 km به m</code>"
)

CONVERSIONS = {
    ("km", "m"): lambda x: x * 1000,
    ("m", "km"): lambda x: x / 1000,
    ("m", "cm"): lambda x: x * 100,
    ("cm", "m"): lambda x: x / 100,
    ("cm", "mm"): lambda x: x * 10,
    ("mm", "cm"): lambda x: x / 10,
    ("mile", "km"): lambda x: x * 1.60934,
    ("km", "mile"): lambda x: x / 1.60934,
    ("ft", "m"): lambda x: x * 0.3048,
    ("m", "ft"): lambda x: x / 0.3048,
    ("kg", "g"): lambda x: x * 1000,
    ("g", "kg"): lambda x: x / 1000,
    ("lb", "kg"): lambda x: x * 0.453592,
    ("kg", "lb"): lambda x: x / 0.453592,
    ("c", "f"): lambda x: x * 9 / 5 + 32,
    ("f", "c"): lambda x: (x - 32) * 5 / 9,
    ("c", "k"): lambda x: x + 273.15,
    ("k", "c"): lambda x: x - 273.15,
}


async def weather(update, context):
    if not context.args:
        await update.message.reply_text(
            "🌤 نام شهر رو بنویس:\nمثال: <code>/weather Tehran</code>",
            parse_mode="HTML"
        )
        return
    city = " ".join(context.args)
    API_KEY = ""  # اینجا API key از weatherapi.com بذار
    if not API_KEY:
        await update.message.reply_text(
            f"🌤 <b>آب و هوای {city}</b>\n\n"
            "⚠️ برای فعال‌سازی این بخش یه API key رایگان از\n"
            "weatherapi.com بگیر و توی modules/useful.py جایگزین کن.",
            parse_mode="HTML"
        )
        return
    try:
        async with aiohttp.ClientSession() as session:
            url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&lang=fa"
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status != 200:
                    await update.message.reply_text("❌ شهر پیدا نشد.")
                    return
                data = await resp.json()
        loc = data["location"]["name"]
        temp_c = data["current"]["temp_c"]
        feels = data["current"]["feelslike_c"]
        condition = data["current"]["condition"]["text"]
        humidity = data["current"]["humidity"]
        wind = data["current"]["wind_kph"]
        await update.message.reply_text(
            f"🌤 <b>آب و هوای {loc}</b>\n"
            f"{'─' * 20}\n"
            f"🌡 دما: {temp_c}°C (احساس: {feels}°C)\n"
            f"☁️ وضعیت: {condition}\n"
            f"💧 رطوبت: {humidity}%\n"
            f"💨 باد: {wind} km/h",
            parse_mode="HTML"
        )
    except Exception:
        await update.message.reply_text("❌ خطا در دریافت اطلاعات آب‌وهوا.")


async def translate(update, context):
    if not context.args:
        await update.message.reply_text(
            "🌐 متن رو بنویس:\nمثال: <code>/translate Hello world</code>",
            parse_mode="HTML"
        )
        return
    text = " ".join(context.args)
    try:
        from deep_translator import GoogleTranslator
        result = GoogleTranslator(source='auto', target='fa').translate(text)
        await update.message.reply_text(
            f"🌐 <b>ترجمه:</b>\n\n"
            f"📝 اصلی: {text}\n"
            f"✅ فارسی: {result}",
            parse_mode="HTML"
        )
    except ImportError:
        await update.message.reply_text(
            "⚠️ کتابخونه ترجمه نصب نیست.\n"
            "<code>pip install deep-translator</code>",
            parse_mode="HTML"
        )
    except Exception:
        await update.message.reply_text("❌ خطا در ترجمه. دوباره امتحان کن.")


async def calculate(update, context):
    if not context.args:
        await update.message.reply_text(
            "🔢 <b>حساب‌گر</b>\n\nمثال: <code>/calc 25 * 4 + 10</code>",
            parse_mode="HTML"
        )
        return
    expr = " ".join(context.args)
    try:
        clean = re.sub(r'[^0-9+\-*/().\s]', '', expr)
        if not clean.strip():
            await update.message.reply_text("❌ عبارت معتبر نیست.")
            return
        result = eval(clean)
        await update.message.reply_text(
            f"🔢 <b>{expr} = {result}</b>",
            parse_mode="HTML"
        )
    except ZeroDivisionError:
        await update.message.reply_text("❌ تقسیم بر صفر مجاز نیست.")
    except Exception:
        await update.message.reply_text(
            "❌ عبارت معتبر نیست.\nمثال: <code>/calc 25 * 4 + 10</code>",
            parse_mode="HTML"
        )


async def convert_unit(update, context):
    if not context.args:
        await update.message.reply_text(UNIT_HELP, parse_mode="HTML")
        return
    text = " ".join(context.args).lower().strip()
    pattern = r'([\d.]+)\s*(\w+)\s*(?:به|to)\s*(\w+)'
    m = re.match(pattern, text)
    if not m:
        await update.message.reply_text(UNIT_HELP, parse_mode="HTML")
        return
    val = float(m.group(1))
    from_unit = m.group(2)
    to_unit = m.group(3)
    key = (from_unit, to_unit)
    if key in CONVERSIONS:
        result = CONVERSIONS[key](val)
        await update.message.reply_text(
            f"✅ <b>{val} {from_unit} = {round(result, 4)} {to_unit}</b>",
            parse_mode="HTML"
        )
    else:
        await update.message.reply_text(
            f"❌ تبدیل {from_unit} به {to_unit} پشتیبانی نمیشه.\n\n{UNIT_HELP}",
            parse_mode="HTML"
        )


async def useful_handler(update, context):
    text = update.message.text.strip()
    for emoji in ["🌤", "🌐", "🔢", "📐"]:
        text = text.replace(emoji, "").strip()

    if "آب و هوا" in text:
        await update.message.reply_text(
            "🌤 نام شهر رو بنویس:\nمثال: <code>/weather Tehran</code>",
            parse_mode="HTML"
        )
    elif "ترجمه" in text:
        await update.message.reply_text(
            "🌐 متن رو بنویس:\nمثال: <code>/translate Hello world</code>",
            parse_mode="HTML"
        )
    elif "حساب" in text:
        await update.message.reply_text(
            "🔢 <b>حساب‌گر</b>\n\nمثال: <code>/calc 25 * 4 + 10</code>",
            parse_mode="HTML"
        )
    elif "تبدیل" in text:
        await update.message.reply_text(UNIT_HELP, parse_mode="HTML")
