import json
import os
from datetime import datetime, date

FILE = "bank.json"


def load():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_account(user):
    data = load()
    uid = str(user.id)
    if uid not in data:
        data[uid] = {
            "name": user.first_name,
            "wallet": 0,
            "bank": 0,
            "loan": 0,
            "last_daily": "",
            "last_interest": ""
        }
        save(data)
    return data[uid]


def update_account(user_id, account):
    data = load()
    data[str(user_id)] = account
    save(data)


# ─── واریز سکه از پیام ─────────────────────────────────
def add_coins_from_message(user, amount=1):
    data = load()
    uid = str(user.id)
    if uid not in data:
        get_account(user)
        data = load()
    data[uid]["wallet"] = data[uid].get("wallet", 0) + amount
    save(data)


# ─── پروفایل بانک ──────────────────────────────────────
async def bank_profile(update, context):
    user = update.effective_user
    acc = get_account(user)

    total = acc["wallet"] + acc["bank"]
    loan = acc.get("loan", 0)

    await update.message.reply_text(
        f"💰 <b>حساب بانکی {user.first_name}</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👛 کیف پول: <b>{acc['wallet']:,}</b> سکه\n"
        f"🏦 بانک: <b>{acc['bank']:,}</b> سکه\n"
        f"💎 دارایی کل: <b>{total:,}</b> سکه\n"
        f"{'📛 وام بدهی: ' + str(loan) + ' سکه' if loan > 0 else '✅ بدون بدهی'}\n\n"
        f"دستورات:\n"
        f"<code>/deposit [مقدار]</code> — واریز به بانک\n"
        f"<code>/withdraw [مقدار]</code> — برداشت از بانک\n"
        f"<code>/transfer @یوزر [مقدار]</code> — انتقال سکه\n"
        f"<code>/daily</code> — جایزه روزانه\n"
        f"<code>/loan [مقدار]</code> — درخواست وام",
        parse_mode="HTML"
    )


# ─── واریز به بانک ──────────────────────────────────────
async def deposit(update, context):
    user = update.effective_user
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("مثال: <code>/deposit 100</code>", parse_mode="HTML")
        return

    amount = int(context.args[0])
    acc = get_account(user)

    if acc["wallet"] < amount:
        await update.message.reply_text(
            f"❌ سکه کافی نداری!\nکیف پول: {acc['wallet']:,} سکه"
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


# ─── برداشت از بانک ─────────────────────────────────────
async def withdraw(update, context):
    user = update.effective_user
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("مثال: <code>/withdraw 100</code>", parse_mode="HTML")
        return

    amount = int(context.args[0])
    acc = get_account(user)

    if acc["bank"] < amount:
        await update.message.reply_text(
            f"❌ موجودی بانک کافی نیست!\nبانک: {acc['bank']:,} سکه"
        )
        return

    acc["bank"] -= amount
    acc["wallet"] += amount
    update_account(user.id, acc)

    await update.message.reply_text(
        f"✅ <b>{amount:,}</b> سکه از بانک برداشت شد.\n"
        f"👛 کیف پول: {acc['wallet']:,} سکه",
        parse_mode="HTML"
    )


# ─── جایزه روزانه ───────────────────────────────────────
async def daily(update, context):
    user = update.effective_user
    acc = get_account(user)
    today = str(date.today())

    if acc.get("last_daily") == today:
        await update.message.reply_text(
            "⏰ جایزه روزانه رو امروز گرفتی!\nفردا دوباره بیا 😊"
        )
        return

    reward = 50
    acc["wallet"] += reward
    acc["last_daily"] = today
    update_account(user.id, acc)

    await update.message.reply_text(
        f"🎁 <b>جایزه روزانه!</b>\n\n"
        f"✅ {reward} سکه به کیف پولت اضافه شد\n"
        f"👛 موجودی: {acc['wallet']:,} سکه",
        parse_mode="HTML"
    )


# ─── انتقال سکه ─────────────────────────────────────────
async def transfer(update, context):
    user = update.effective_user

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ روی پیام کاربر موردنظر ریپلای کن و مقدار رو بنویس:\n"
            "<code>/transfer 100</code>",
            parse_mode="HTML"
        )
        return

    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("مثال: <code>/transfer 100</code>", parse_mode="HTML")
        return

    amount = int(context.args[0])
    target = update.message.reply_to_message.from_user

    if target.id == user.id:
        await update.message.reply_text("❌ نمیتونی به خودت سکه بفرستی!")
        return

    sender = get_account(user)
    if sender["wallet"] < amount:
        await update.message.reply_text(
            f"❌ سکه کافی نداری!\nکیف پول: {sender['wallet']:,} سکه"
        )
        return

    receiver = get_account(target)
    sender["wallet"] -= amount
    receiver["wallet"] += amount
    update_account(user.id, sender)
    update_account(target.id, receiver)

    await update.message.reply_text(
        f"✅ <b>{amount:,}</b> سکه به <b>{target.first_name}</b> منتقل شد!\n"
        f"👛 موجودی شما: {sender['wallet']:,} سکه",
        parse_mode="HTML"
    )


# ─── وام ────────────────────────────────────────────────
async def loan(update, context):
    user = update.effective_user
    acc = get_account(user)

    if acc.get("loan", 0) > 0:
        await update.message.reply_text(
            f"❌ ابتدا وام قبلیت رو پس بده!\n"
            f"📛 بدهی: {acc['loan']:,} سکه\n"
            f"<code>/payloan</code> برای پرداخت",
            parse_mode="HTML"
        )
        return

    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text(
            "🏦 <b>سیستم وام</b>\n\n"
            "حداکثر وام: ۵۰۰ سکه\n"
            "بهره: ۱۰٪\n\n"
            "مثال: <code>/loan 200</code>",
            parse_mode="HTML"
        )
        return

    amount = int(context.args[0])
    if amount > 500:
        await update.message.reply_text("❌ حداکثر وام ۵۰۰ سکه است.")
        return

    payback = int(amount * 1.1)
    acc["wallet"] += amount
    acc["loan"] = payback
    update_account(user.id, acc)

    await update.message.reply_text(
        f"✅ وام <b>{amount:,}</b> سکه دریافت شد!\n"
        f"📛 باید <b>{payback:,}</b> سکه پس بدی (۱۰٪ بهره)\n"
        f"<code>/payloan</code> برای پرداخت وام",
        parse_mode="HTML"
    )


# ─── پرداخت وام ─────────────────────────────────────────
async def payloan(update, context):
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

