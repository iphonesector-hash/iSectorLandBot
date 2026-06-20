import re


# ─── حساب‌گر ───────────────────────────────────────────
def calculate(expr: str) -> str:
    """حساب‌گر ساده"""
    try:
        # فقط اعداد و عملگرها مجاز هستن
        clean = re.sub(r'[^0-9+\-*/().% ]', '', expr)
        if not clean.strip():
            return "❌ عبارت معتبر نیست."
        result = eval(clean)
        return f"🔢 نتیجه: <b>{expr} = {result}</b>"
    except ZeroDivisionError:
        return "❌ تقسیم بر صفر مجاز نیست."
    except:
        return "❌ عبارت ریاضی معتبر نیست.\nمثال: <code>25 * 4 + 10</code>"


# ─── تبدیل واحد ────────────────────────────────────────
UNIT_HELP = (
    "📐 <b>تبدیل واحد</b>\n\n"
    "فرمت: <code>مقدار واحد به واحد</code>\n\n"
    "<b>طول:</b>\n"
    "km → m, m → cm, cm → mm\n"
    "mile → km, km → mile\n"
    "ft → m, m → ft\n\n"
    "<b>وزن:</b>\n"
    "kg → g, g → kg\n"
    "lb → kg, kg → lb\n\n"
    "<b>دما:</b>\n"
    "c → f, f → c, c → k, k → c\n\n"
    "مثال: <code>100 km به m</code>"
)

conversions = {
    # طول
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
    # وزن
    ("kg", "g"): lambda x: x * 1000,
    ("g", "kg"): lambda x: x / 1000,
    ("lb", "kg"): lambda x: x * 0.453592,
    ("kg", "lb"): lambda x: x / 0.453592,
    # دما
    ("c", "f"): lambda x: x * 9/5 + 32,
    ("f", "c"): lambda x: (x - 32) * 5/9,
    ("c", "k"): lambda x: x + 273.15,
    ("k", "c"): lambda x: x - 273.15,
}

def convert_unit(text: str) -> str:
    """
    ورودی: "100 km به m"
    """
    text = text.lower().strip()
    pattern = r'([\d.]+)\s*(\w+)\s*(?:به|to)\s*(\w+)'
    m = re.match(pattern, text)
    if not m:
        return UNIT_HELP

    val = float(m.group(1))
    from_unit = m.group(2)
    to_unit = m.group(3)

    key = (from_unit, to_unit)
    if key in conversions:
        result = conversions[key](val)
        return f"✅ <b>{val} {from_unit} = {round(result, 4)} {to_unit}</b>"
    else:
        return f"❌ تبدیل از {from_unit} به {to_unit} پشتیبانی نمیشه.\n\n{UNIT_HELP}"


# ─── آب و هوا (نیاز به API key) ───────────────────────
async def weather(update, context):
    if not context.args:
        await update.message.reply_text(
            "🌤 برای دریافت آب‌وهوا، نام شهر رو بنویس:\n"
            "مثال: <code>/weather Tehran</code>",
            parse_mode="HTML"
        )
        return

    city = " ".join(context.args)

    # اگه API key داری اینجا بذار
    API_KEY = ""  # weatherapi.com یا openweathermap.org

    if not API_KEY:
        await update.message.reply_text(
            f"🌤 <b>آب و هوای {city}</b>\n\n"
            "⚠️ برای فعال‌سازی این بخش، یه API key رایگان از\n"
            "weatherapi.com بگیر و توی modules/useful.py جایگزین کن.",
            parse_mode="HTML"
        )
        return

    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&lang=fa"
            async with session.get(url) as resp:
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
    except Exception as e:
        await update.message.reply_text("❌ خطا در دریافت اطلاعات آب‌وهوا.")


# ─── ترجمه ─────────────────────────────────────────────
async def translate(update, context):
    if not context.args:
        await update.message.reply_text(
            "🌐 <b>ترجمه متن</b>\n\n"
            "متن مورد نظرت رو بفرست:\n"
            "مثال: <code>/translate Hello how are you</code>\n\n"
            "⚠️ برای استفاده از این بخش باید کتابخونه\n"
            "<code>deep_translator</code> نصب باشه:\n"
            "<code>pip install deep-translator</code>",
            parse_mode="HTML"
        )
        return

    text = " ".join(context.args)

    try:
        from deep_translator import GoogleTranslator
        result = GoogleTranslator(source='auto', target='fa').translate(text)
        await update.message.reply_text(
            f"🌐 <b>ترجمه:</b>\n\n"
            f"📝 متن اصلی: {text}\n"
            f"✅ ترجمه: {result}",
            parse_mode="HTML"
        )
    except ImportError:
        await update.message.reply_text(
            "⚠️ کتابخونه ترجمه نصب نیست.\n"
            "اجرا کن: <code>pip install deep-translator</code>",
            parse_mode="HTML"
        )
    except Exception:
        await update.message.reply_text("❌ خطا در ترجمه. دوباره امتحان کن.")


async def useful_handler(update, context):
    """هندلر اصلی بخش کاربردی"""
    text = update.message.text.strip()

    if text == "🌤 آب و هوا":
        await update.message.reply_text(
            "🌤 نام شهر رو بنویس:\nمثال: <code>/weather Tehran</code>",
            parse_mode="HTML"
        )

    elif text == "🌐 ترجمه":
        await update.message.reply_text(
            "🌐 متن رو بنویس:\nمثال: <code>/translate Hello world</code>",
            parse_mode="HTML"
        )

    elif text == "🔢 حساب‌گر":
        await update.message.reply_text(
            "🔢 <b>حساب‌گر</b>\n\n"
            "عملیات ریاضی رو بنویس:\n"
            "مثال: <code>/calc 25 * 4 + 10</code>",
            parse_mode="HTML"
        )

    elif text == "📐 تبدیل واحد":
        await update.message.reply_text(UNIT_HELP, parse_mode="HTML")

