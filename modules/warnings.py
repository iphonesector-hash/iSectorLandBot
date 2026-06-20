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



def get_data():

    return load()



def get_user_warn(chat_id, user_id):

    data = load()

    chat = str(chat_id)
    user = str(user_id)

    if chat not in data:
        data[chat] = {}

    if user not in data[chat]:
        data[chat][user] = 0

    return data



async def warn(update, context):

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ روی پیام کاربر ریپلای کن"
        )
        return


    user = update.message.reply_to_message.from_user
    chat = update.effective_chat


    data = get_user_warn(
        chat.id,
        user.id
    )


    data[str(chat.id)][str(user.id)] += 1

    count = data[str(chat.id)][str(user.id)]

    save(data)


    await update.message.reply_text(
        f"⚠️ اخطار ثبت شد\n\n"
        f"👤 {user.first_name}\n"
        f"🔢 تعداد: {count}/3"
    )


    if count >= 3:

        try:
            await chat.ban_member(user.id)

            await update.message.reply_text(
                "🚫 کاربر با ۳ اخطار بن شد"
            )

        except:

            await update.message.reply_text(
                "❌ دسترسی بن ندارم"
            )



async def clear_warn(update, context):

    if not update.message.reply_to_message:

        await update.message.reply_text(
            "🧹 روی پیام کاربر ریپلای کن"
        )

        return


    user = update.message.reply_to_message.from_user
    chat = update.effective_chat


    data = get_user_warn(
        chat.id,
        user.id
    )


    data[str(chat.id)][str(user.id)] = 0

    save(data)


    await update.message.reply_text(
        f"🧹 اخطارهای {user.first_name} پاک شد"
    )



# سازگاری با admin.py قدیمی
add_warn = warn
remove_warn = clear_warn
