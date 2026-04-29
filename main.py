import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

# --- FLASK SERVER ---
flask_app = Flask('')

@flask_app.route('/')
def home():
    return "Bot is live!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

keep_alive()

# --- TELEGRAM BOT ---
TOKEN = os.getenv("TOKEN")

movies = {
    "demo": {
        "name": "demo post movie by krish basak",
        "language": "Hindi",
        "files": {
            "480p": "BAACAgUAAxkBAAFIUHdp8Qk-t92K7GF6RAOD1uD-JVNRnQACgx4AAiswiFcRv6lJQIOxHzsE",
            "720p": "BAACAgUAAxKBAAFIUHdp8Qk-t92K7GF6RAOD1UD-JVNRnQACgx4AAiswiFcRv6lJQIOxHzsE",
            "1080p": "BAACAgUAAxkBAAFIWVRp8cYwZqbzwWKTug4-CZGLoFJE_AACDSUAAk_CkVcyCAjewtV3-jsE"
        }
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_id = update.effective_user.id
    text = update.message.text.split()
    
    if len(text) > 1:
        key = text[1].lower()
        if key in movies:
            movie_data = movies[key]
            
            # Jodi multiple files thake
            if isinstance(movie_data, dict) and "files" in movie_data:
                m_name = movie_data.get("name", "Unknown Movie")
                m_lang = movie_data.get("language", "Hindi")
                
                # Ei loop-tai tintai video pathabe
                for quality, f_id in movie_data["files"].items():
                    caption_text = (
                        f"🎬 **Movie:** {m_name}\n"
                        f"🔊 **Language:** {m_lang}\n"
                        f"💿 **Quality:** {quality}\n\n"
                        f"🍿 Enjoy your movie!"
                    )
                    
                    try:
                        await context.bot.send_video(
                            chat_id=user_id,
                            video=f_id,
                            caption=caption_text,
                            parse_mode="Markdown"
                        )
                        # Ekta chhoto gap dewa jate Telegram spam mone na kore
                        await asyncio.sleep(1) 
                    except Exception as e:
                        print(f"Error sending {quality}: {e}")
            
            # Jodi purono simple style hoy
            else:
                await context.bot.send_video(
                    chat_id=user_id,
                    video=movie_data,
                    caption="Here is your movie! 🍿"
                )
        else:
            await update.message.reply_text("Movie not found ❌")
    else:
        await update.message.reply_text("Please use a valid link!")

# Application Build
bot_app = ApplicationBuilder().token(TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))

if __name__ == '__main__':
    print("Bot is starting... 🚀")
    bot_app.run_polling()
