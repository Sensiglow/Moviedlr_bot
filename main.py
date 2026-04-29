import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

# --- FLASK SERVER FOR RENDER ---
flask_app = Flask('')

@flask_app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# Server start koro
keep_alive()

# --- TELEGRAM BOT LOGIC ---
TOKEN = os.getenv("TOKEN")

movies = {
    "krish3": "BAACAgUAAxkBAAFIUHdp8Qk-t92K7GF6RAOD1uD-JVNRnQACgx4AAiswiFcRv6lJQIOxHzsE"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if context.args:
        key = context.args[0].lower()
        if key in movies:
            msg = await context.bot.send_video(
                chat_id=user_id,
                video=movies[key],
                caption="⏳ File will be removed in 1 hour"
            )
            # 1 hour pore delete korar logic
            await asyncio.sleep(3600)
            await context.bot.delete_message(
                chat_id=user_id,
                message_id=msg.message_id
            )
        else:
            await update.message.reply_text("Movie not found ❌")
    else:
        await update.message.reply_text("Send valid link")

# Bot Application setup (Variable name changed to bot_app)
bot_app = ApplicationBuilder().token(TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))

print("Bot is running... 🚀")
bot_app.run_polling()
