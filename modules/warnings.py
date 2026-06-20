import json
import os


FILE = "warnings.json"


def load():

    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)



def save(data):

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )



def get_warn(chat_id, user_id):

    data = load()

    chat = str(chat_id)
    user = str(user_id)

    if chat not in data:
        data[chat] = {}

    if user not in data[chat]:
        data[chat][user] = 0

    return data[chat][user]



def set_warn(chat_id, user_id, amount):

    data = load()

    chat = str(chat_id)
    user = str(user_id)

    if chat not in data:
        data[chat] = {}

    data[chat][user] = amount

    save(data)



def add_warn(chat_id, user_id):

    count = get_warn(chat_id, user_id)

    count += 1

    set_warn(
        chat_id,
        user_id,
        count
    )

    return count



def remove_warn(chat_id, user_id):

    set_warn(
        chat_id,
        user_id,
        0
    )



async def warn(update, context):

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ روی پیام کاربر ریپلای کن"
        )
        return


    user = update.message.reply_to_message.from_user
    chat = update.effective_chat


    count = add_warn(
        chat.id,
        user.id
    )


    await update.message.reply_text(
        f"⚠️ اخطار ثبت شد\n\n"
        f"👤 {user.first_name}\n"
        f"🔢 {count}/3"
    )


    if count >= 3:

        try:
            await chat.ban_member(user.id)

            await update.message.reply_text(
                "🚫 کاربر با ۳ اخطار بن شد"
            )

        except:

            pass



async def clear_warn(update, context):

    if not update.message.reply_to_message:
        return


    user = update.message.reply_to_message.from_user
    chat = update.effective_chat


    remove_warn(
        chat.id,
        user.id
    )


    await update.message.reply_text(
        "🧹 اخطارها پاک شد"
    )
