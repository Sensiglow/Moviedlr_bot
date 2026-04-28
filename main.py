from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import os

TOKEN = os.getenv("8787269105:AAGlmHg0gAl7laBGj86hAXnJtus8KblRFAE")

movies = {
    "krish3": "AAMCBQADGQEDDbilafDunOnoxxNtkvWBPMopKcBirIwAAoMeAAIrMIhXtXbv2vuERtkBAAdtAAM7BA"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if context.args:
        key = context.args[0]

        if key in movies:
            msg = await context.bot.send_video(
                chat_id=user_id,
                video=movies[key],
                caption="⏳ File will be removed in 1 hour"
            )

            await asyncio.sleep(3600)
            await context.bot.delete_message(chat_id=user_id, message_id=msg.message_id)

        else:
            await update.message.reply_text("Movie not found ❌")
    else:
        await update.message.reply_text("Send valid link")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
