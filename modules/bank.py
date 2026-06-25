import json
import os
from datetime import date

FILE = "bank.json"


def load() -> dict:
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data: dict):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_account(user) -> dict:
    data = load()
    uid = str(user.id)
    if uid not in data:
        data[uid] = {
            "name": user.first_name,
            "wallet": 0,
            "bank": 0,
            "loan": 0,
            "last_daily": "",
        }
        save(data)
    else:
        data[uid]["name"] = user.first_name
        save(data)
    return data[uid]


def update_account(user_id, account: dict):
    data = load()
    data[str(user_id)] = account
    save(data)


def add_coins_from_message(user, amount: int = 1):
    data = load()
    uid = str(user.id)
    if uid not in data:
        get_account(user)
        data = load()
    data[uid]["wallet"] = data[uid].get("wallet", 0) + amount
    save(data)


# ─── نمایش کیف پول ─────────────────────────────────────
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
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📌 دستورات:\n"
        f"/deposit [مقدار] — واریز به بانک\n"
        f"/withdraw [مقدار] — برداشت از بانک\n"
        f"/transfer [مقدار] — انتقال سکه (ریپلای)\n"
        f"/loan [مقدار] — درخواست وام\n"
        f"/payloan — پرداخت وام\n"
        f"/daily — جایزه روزانه",
        parse_mode="HTML"
    )


# ─── واریز به بانک ──────────────────────────────────────
async def deposit(update, context):
    user = update.effective_user
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text(
            "💳 مثال: <code>/deposit 100</code>", parse_mode="HTML"
        )
        return
    amount = int(context.args[0])
    if amount <= 0:
        await update.message.reply_text("❌ مقدار باید بیشتر از صفر باشه.")
        return
    acc = get_account(user)
    if acc["wallet"] < amount:
        await update.message.reply_text(
            f"❌ سکه کافی نداری!\n👛 کیف پول: {acc['wallet']:,} سکه"
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
        await update.message.reply_text(
            "💳 مثال: <code>/withdraw 100</code>", parse_mode="HTML"
        )
        return
    amount = int(context.args[0])
    if amount <= 0:
        await update.message.reply_text("❌ مقدار باید بیشتر از صفر باشه.")
        return
    acc = get_account(user)
    if acc["bank"] < amount:
        await update.message.reply_text(
            f"❌ موجودی بانک کافی نیست!\n🏦 بانک: {acc['bank']:,} سکه"
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
            "↩️ روی پیام کاربر موردنظر ریپلای کن و بنویس:\n"
            "<code>/transfer 100</code>",
            parse_mode="HTML"
        )
        return
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text(
            "💳 مثال: <code>/transfer 100</code>", parse_mode="HTML"
        )
        return
    amount = int(context.args[0])
    if amount <= 0:
        await update.message.reply_text("❌ مقدار باید بیشتر از صفر باشه.")
        return
    target = update.message.reply_to_message.from_user
    if target.id == user.id:
        await update.message.reply_text("❌ نمیتونی به خودت سکه بفرستی!")
        return
    if target.is_bot:
        await update.message.reply_text("❌ نمیتونی به ربات سکه بفرستی!")
        return
    sender = get_account(user)
    if sender["wallet"] < amount:
        await update.message.reply_text(
            f"❌ سکه کافی نداری!\n👛 کیف پول: {sender['wallet']:,} سکه"
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
            f"❌ اول وام قبلیت رو پس بده!\n"
            f"📛 بدهی: {acc['loan']:,} سکه\n"
            f"برای پرداخت: <code>/payloan</code>",
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
    if amount <= 0 or amount > 500:
        await update.message.reply_text("❌ مقدار وام باید بین ۱ تا ۵۰۰ سکه باشه.")
        return
    payback = int(amount * 1.1)
    acc["wallet"] += amount
    acc["loan"] = payback
    update_account(user.id, acc)
    await update.message.reply_text(
        f"✅ وام <b>{amount:,}</b> سکه دریافت شد!\n"
        f"📛 باید <b>{payback:,}</b> سکه پس بدی (۱۰٪ بهره)\n"
        f"برای پرداخت: <code>/payloan</code>",
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


# ─── تاپ ثروتمندان ──────────────────────────────────────
async def rich_leaderboard(update, context):
    data = load()
    if not data:
        await update.message.reply_text("هنوز کسی حساب ندارد.")
        return
    sorted_users = sorted(
        data.items(),
        key=lambda x: x[1].get("wallet", 0) + x[1].get("bank", 0),
        reverse=True
    )[:10]
    medals = ["🥇", "🥈", "🥉"]
    text = "💰 <b>ثروتمندترین‌های سکتورلند</b>\n━━━━━━━━━━━━━━━━━━\n"
    for i, (uid, info) in enumerate(sorted_users):
        medal = medals[i] if i < 3 else f"{i+1}."
        total = info.get("wallet", 0) + info.get("bank", 0)
        text += f"{medal} <b>{info.get('name','کاربر')}</b> — {total:,} سکه\n"
    await update.message.reply_text(text, parse_mode="HTML")
