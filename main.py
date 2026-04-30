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
    # --- MOVIE 1 (Demo) ---
    "demo": {
        "name": "demo post movie by krish basak",
        "language": "Hindi",
        "files": {
            "480p": "BAACAgUAAxkBAAFIUHdp8Qk-t92K7GF6RAOD1uD-JVNRnQACgx4AAiswiFcRv6lJQIOxHzsE",
            "720p": "BAACAgUAAxkBAAFIUHdp8Qk-t92K7GF6RAOD1uD-JVNRnQACgx4AAiswiFcRv6lJQIOxHzsE",
            "1080p": "BAACAgUAAxkBAAFIWVRp8cYwZqbzwWKTug4-CZGLoFJE_AACDSUAAk_CkVcyCAjewtV3-jsE"
        }
    },

    # --- MOVIE 2 ---
    "tereisqmqin": {
        "name": "Tere Isqh Main",
        "language": "Hindi",
        "files": {
            "480p": "BAACAgUAAxkBAAFIaiBp8sMbHJu5kaiLpHAkBWHFWYOPewACJh4AAk_CmVcfEcsr93P4OzsE",
            "720p": "BAACAgUAAxkBAAFIAiRp8sQ52ihQgDlipui60bZCwqqw2QACJx4AAk_CmVcHjaxLPw5e5jsE"
        }
    },

    # --- MOVIE 3 ---
    "movie_key_3": {
        "name": "Movie Name 3",
        "language": "Hindi",
        "files": {
            "480p": "FILE_ID_EKHANE",
            "720p": "FILE_ID_EKHANE",
            "1080p": "FILE_ID_EKHANE"
        }
    },

    # --- MOVIE 4 ---
    "movie_key_4": {
        "name": "Movie Name 4",
        "language": "Hindi",
        "files": {
            "480p": "FILE_ID_EKHANE",
            "720p": "FILE_ID_EKHANE",
            "1080p": "FILE_ID_EKHANE"
        }
    },

    # --- MOVIE 5 ---
    "movie_key_5": {
        "name": "Movie Name 5",
        "language": "Hindi",
        "files": {
            "480p": "FILE_ID_EKHANE",
            "720p": "FILE_ID_EKHANE",
            "1080p": "FILE_ID_EKHANE"
        }
    },

    # --- MOVIE 6 ---
    "movie_key_6": {
        "name": "Movie Name 6",
        "language": "Hindi",
        "files": {
            "480p": "FILE_ID_EKHANE",
            "720p": "FILE_ID_EKHANE",
            "1080p": "FILE_ID_EKHANE"
        }
    },

    # --- MOVIE 7 ---
    "movie_key_7": {
        "name": "Movie Name 7",
        "language": "Hindi",
        "files": {
            "480p": "FILE_ID_EKHANE",
            "720p": "FILE_ID_EKHANE",
            "1080p": "FILE_ID_EKHANE"
        }
    },

    # --- MOVIE 8 ---
    "movie_key_8": {
        "name": "Movie Name 8",
        "language": "Hindi",
        "files": {
            "480p": "FILE_ID_EKHANE",
            "720p": "FILE_ID_EKHANE",
            "1080p": "FILE_ID_EKHANE"
        }
    },

    # --- MOVIE 9 ---
    "movie_key_9": {
        "name": "Movie Name 9",
        "language": "Hindi",
        "files": {
            "480p": "FILE_ID_EKHANE",
            "720p": "FILE_ID_EKHANE",
            "1080p": "FILE_ID_EKHANE"
        }
    },

    # --- MOVIE 10 ---
    "movie_key_10": {
        "name": "Movie Name 10",
        "language": "Hindi",
        "files": {
            "480p": "FILE_ID_EKHANE",
            "720p": "FILE_ID_EKHANE",
            "1080p": "FILE_ID_EKHANE"
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
