import json
import os
from datetime import datetime, date


BANK_FILE = "bank.json"


def load():
    """بارگذاری داده‌های بانک"""
    if not os.path.exists(BANK_FILE):
        return {}
    try:
        with open(BANK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save(data):
    """ذخیره داده‌های بانک"""
    try:
        with open(BANK_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        pass


def get_account(user):
    """دریافت حساب کاربر"""
    data = load()
    uid = str(user.id)
    if uid not in data:
        data[uid] = {
            "name": user.first_name,
            "wallet": 0,
            "bank": 0,
            "investment": 0,
            "loan": 0,
            "last_daily": "",
            "last_interest": "",
            "vip": False
        }
        save(data)
    return data[uid]


def update_account(user_id, account):
    """بروزرسانی حساب کاربر"""
    data = load()
    data[str(user_id)] = account
    save(data)


def add_coins_from_message(user, amount=1):
    """اضافه کردن سکه برای هر پیام"""
    data = load()
    uid = str(user.id)
    if uid not in data:
        get_account(user)
        data = load()
    data[uid]["wallet"] = data[uid].get("wallet", 0) + amount
    save(data)


async def bank_profile(update, context):
    """نمایش پروفایل بانکی"""
    user = update.effective_user
    acc = get_account(user)

    total = acc["wallet"] + acc["bank"] + acc["investment"]
    loan = acc.get("loan", 0)
    vip = "✅ VIP" if acc.get("vip") else "❌ عادی"

    await update.message.reply_text(
        f"💰 <b>حساب بانکی {user.first_name}</b>\n"
        f"{'━' * 30}\n"
        f"👛 کیف پول: <b>{acc['wallet']:,}</b> سکه\n"
        f"🏦 بانک: <b>{acc['bank']:,}</b> سکه\n"
        f"📈 سرمایه‌گذاری: <b>{acc['investment']:,}</b> سکه\n"
        f"💎 دارایی کل: <b>{total:,}</b> سکه\n"
        f"{'📛 بدهی: ' + str(loan) + ' سکه' if loan > 0 else '✅ بدون بدهی'}\n"
        f"🌟 وضعیت: {vip}\n"
        f"{'━' * 30}\n"
        f"<b>دستورات:</b>\n"
        f"<code>/deposit [عدد]</code> - واریز به بانک\n"
        f"<code>/withdraw [عدد]</code> - برداشت از بانک\n"
        f"<code>/daily</code> - جایزه روزانه (50 سکه)\n"
        f"<code>/invest [عدد]</code> - سرمایه‌گذاری\n"
        f"<code>/loan [عدد]</code> - درخواست وام",
        parse_mode="HTML"
    )


async def deposit(update, context):
    """واریز به بانک"""
    user = update.effective_user
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text(
            "💰 <b>واریز به بانک</b>\n"
            "مثال: <code>/deposit 100</code>",
            parse_mode="HTML"
        )
        return

    amount = int(context.args[0])
    if amount <= 0:
        await update.message.reply_text("❌ مقدار باید بزرگ‌تر از صفر باشد.")
        return

    acc = get_account(user)

    if acc["wallet"] < amount:
        await update.message.reply_text(
            f"❌ سکه کافی نداری!\n👛 موجودی: {acc['wallet']:,} سکه"
        )
        return

    acc["wallet"] -= amount
    acc["bank"] += amount
    update_account(user.id, acc)

    await update.message.reply_text(
        f"✅ <b>{amount:,}</b> سکه به بانک واریز شد.\n"
        f"🏦 موجودی بانک: {acc['bank']:,} سکه",
        parse_mode="HTML"
    )


async def withdraw(update, context):
    """برداشت از بانک"""
    user = update.effective_user
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text(
            "💰 <b>برداشت از بانک</b>\n"
            "مثال: <code>/withdraw 100</code>",
            parse_mode="HTML"
        )
        return

    amount = int(context.args[0])
    if amount <= 0:
        await update.message.reply_text("❌ مقدار باید بزرگ‌تر از صفر باشد.")
        return

    acc = get_account(user)

    if acc["bank"] < amount:
        await update.message.reply_text(
            f"❌ موجودی بانک کافی نیست!\n🏦 موجودی: {acc['bank']:,} سکه"
        )
        return

    acc["bank"] -= amount
    acc["wallet"] += amount
    update_account(user.id, acc)

    await update.message.reply_text(
        f"✅ <b>{amount:,}</b> سکه برداشت شد.\n"
        f"👛 کیف پول: {acc['wallet']:,} سکه",
        parse_mode="HTML"
    )


async def daily(update, context):
    """جایزه روزانه"""
    user = update.effective_user
    acc = get_account(user)
    today = str(date.today())

    if acc.get("last_daily") == today:
        await update.message.reply_text(
            "⏰ جایزه روزانه رو امروز گرفتی!\n"
            "فردا دوباره بیا 😊"
        )
        return

    reward = 50
    vip_bonus = 25 if acc.get("vip") else 0
    total_reward = reward + vip_bonus

    acc["wallet"] += total_reward
    acc["last_daily"] = today
    update_account(user.id, acc)

    await update.message.reply_text(
        f"🎁 <b>جایزه روزانه!</b>\n\n"
        f"✅ {reward} سکه جایزه پایه\n"
        f"{'💎 +' + str(vip_bonus) + ' سکه بونوس VIP' if vip_bonus > 0 else ''}\n"
        f"💰 <b>جمع: {total_reward} سکه</b>\n"
        f"👛 موجودی فعلی: {acc['wallet']:,} سکه",
        parse_mode="HTML"
    )


async def invest(update, context):
    """سرمایه‌گذاری"""
    user = update.effective_user
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text(
            "📈 <b>سرمایه‌گذاری</b>\n\n"
            "بازده ماهانه: 15٪\n"
            "حداقل: 100 سکه\n\n"
            "مثال: <code>/invest 200</code>",
            parse_mode="HTML"
        )
        return

    amount = int(context.args[0])
    if amount < 100:
        await update.message.reply_text("❌ حداقل سرمایه‌گذاری 100 سکه است.")
        return

    acc = get_account(user)

    if acc["wallet"] < amount:
        await update.message.reply_text(
            f"❌ سکه کافی نداری!\n👛 موجودی: {acc['wallet']:,} سکه"
        )
        return

    acc["wallet"] -= amount
    acc["investment"] += amount
    update_account(user.id, acc)

    expected_return = int(amount * 0.15)

    await update.message.reply_text(
        f"📈 <b>سرمایه‌گذاری موفق!</b>\n\n"
        f"✅ مبلغ: <b>{amount:,}</b> سکه\n"
        f"💰 بازده ماهانه: <b>~{expected_return:,}</b> سکه (15٪)\n"
        f"📊 کل سرمایه: {acc['investment']:,} سکه",
        parse_mode="HTML"
    )


async def loan(update, context):
    """درخواست وام"""
    user = update.effective_user
    acc = get_account(user)

    if acc.get("loan", 0) > 0:
        await update.message.reply_text(
            f"❌ ابتدا وام قبلی رو پس بده!\n"
            f"📛 بدهی: {acc['loan']:,} سکه\n"
            f"<code>/payloan</code> برای پرداخت",
            parse_mode="HTML"
        )
        return

    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text(
            "🏦 <b>سیستم وام</b>\n\n"
            "حداکثر وام: 1000 سکه\n"
            "بهره: 15٪\n\n"
            "مثال: <code>/loan 500</code>",
            parse_mode="HTML"
        )
        return

    amount = int(context.args[0])
    if amount > 1000:
        await update.message.reply_text("❌ حداکثر وام 1000 سکه است.")
        return

    if amount < 50:
        await update.message.reply_text("❌ حداقل وام 50 سکه است.")
        return

    payback = int(amount * 1.15)
    acc["wallet"] += amount
    acc["loan"] = payback
    update_account(user.id, acc)

    await update.message.reply_text(
        f"✅ وام <b>{amount:,}</b> سکه دریافت شد!\n"
        f"📛 باید <b>{payback:,}</b> سکه پس بدی (15٪ بهره)\n"
        f"<code>/payloan</code> برای پرداخت",
        parse_mode="HTML"
    )


async def payloan(update, context):
    """پرداخت وام"""
    user = update.effective_user
    acc = get_account(user)
    loan_amount = acc.get("loan", 0)

    if loan_amount == 0:
        await update.message.reply_text("✅ وامی نداری!")
        return

    if acc["wallet"] < loan_amount:
        await update.message.reply_text(
            f"❌ سکه کافی نداری!\n"
            f"👛 کیف پول: {acc['wallet']:,} سکه\n"
            f"📛 بدهی: {loan_amount:,} سکه"
        )
        return

    acc["wallet"] -= loan_amount
    acc["loan"] = 0
    update_account(user.id, acc)

    await update.message.reply_text(
        f"✅ وام <b>{loan_amount:,}</b> سکه پرداخت شد!\n"
        f"👛 موجودی: {acc['wallet']:,} سکه",
        parse_mode="HTML"
    )
