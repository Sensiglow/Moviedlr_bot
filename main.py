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
    "krish3": "BAACAgUAAxkBAAFIWVRp8cYwZqbzwWKTug4-CZGLoFJE_AACDSUAAk_CkVcyCAjewtV3-jsE"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Message-er bhetore text check koro (e.g., /start krish3)
    text = update.message.text.split()
    
    if len(text) > 1:
        key = text[1].lower() 
        
        if key in movies:
            await context.bot.send_video(
                chat_id=user_id,
                video=movies[key],
                caption="Here is your movie! 🍿"
            )
            # Delete logic ekhon-kar moto off rakha holo test korar jonno
            # await asyncio.sleep(3600)
            # await context.bot.delete_message(chat_id=user_id, message_id=msg.message_id)
            except:
                pass # Jodi user agei delete kore dey, tobe error skip korbe
        else:
            await update.message.reply_text("Movie not found ❌")
    else:
        await update.message.reply_text("Please use a valid link to get the movie!")

# Bot Application setup (Variable name changed to bot_app)
bot_app = ApplicationBuilder().token(TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))

print("Bot is running... 🚀")
bot_app.run_polling()
