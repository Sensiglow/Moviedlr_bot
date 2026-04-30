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

# Movie List
movies = {
    "demo": {
        "name": "demo post movie by krish basak",
        "language": "Hindi",
        "files": {
            "480p": "BAACAgUAAxkBAAFIUHdp8Qk-t92K7GF6RAOD1uD-JVNRnQACgx4AAiswiFcRv6lJQIOxHzsE",
            "720p": "BAACAgUAAxkBAAFIUHdp8Qk-t92K7GF6RAOD1uD-JVNRnQACgx4AAiswiFcRv6lJQIOxHzsE",
            "1080p": "BAACAgUAAxkBAAFIWVRp8cYwZqbzwWKTug4-CZGLoFJE_AACDSUAAk_CkVcyCAjewtV3-jsE"
        }
    },
    "tereisqmqin": {
        "name": "Tere Isqh Main",
        "language": "Hindi",
        "files": {
            "480p": "BAACAgUAAxkBAAFIaiBp8sMbHJu5kaiLpHAkBWHFWYOPewACJh4AAk_CmVcfEcsr93P4OzsE",
            "720p": "BAACAgUAAxkBAAFIAiRp8sQ52ihQgDlipui60bZCwqqw2QACJx4AAk_CmVcHjaxLPw5e5jsE"
        }
    },
    "cmbharat": {
        "name": "Dashing Cm Bharat new hindi Movie",
        "language": "Hindi",
        "files": {
            "480p": "BQACAgUAAXKBAAFIc0tp8217bhPVBb50YIDUP7G1PEXWNQACVSIAAK_CoVf59wa5ZzZJVjsE",
            "720p": "BQACAgUAAXKBAAFIc4Np82XgifXon0m65a_ydVGJlbiP1gACwCIAAK_CoVdypev9J3Th9TsE",
            "1080p": "BQACAgUAAXKBAAFic4xp82YAAco9R17dcKBpixINsbXOMtgAAsMiAAJPwqFXg9mBr5K9hyk7BA"
        }
    }
}

async def delete_message(context: ContextTypes.DEFAULT_TYPE):
    """Nirdishto somoy por message delete korbe"""
    job = context.job
    try:
        await context.bot.delete_message(chat_id=job.chat_id, message_id=job.data)
    except Exception as e:
        print(f"Delete Error: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_id = update.effective_user.id
    text = update.message.text.split()
    
    # Jodi keu shudhu /start likhe (kono key na thake)
    if len(text) == 1:
        help_text = (
            "👋 **Welcome to MovieDLR Bot!**\n\n"
            "Ami apnake movies download korte sahajyo kori. Movie pete channel-er link-e click korun.\n\n"
            "⚠️ **Sotorkobarta:**\n"
            "Copyright karone amader bot theke dewa prottekta video **24 ghonta** por automatic delete hoye jabe. Tai druto download ba save kore nin!"
        )
        await update.message.reply_text(help_text, parse_mode="Markdown")
        return

    # Jodi key thake (e.g., /start cmbharat)
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_id = update.effective_user.id
    text = update.message.text.split()
    
    # 1. Sudhu /start korle Welcome Message + Hint
    if len(text) == 1:
        help_text = (
            "👋 **Welcome to the Download Bot!**\n\n"
            "Ami apnake Movie, Series ebong shob dhoroner Files download korte sahajyo kori.\n\n"
            "🍿 **Kivabe use korben?**\n"
            "Channel-er link-e click korun ba `/start movie_key` likhun.\n\n"
            "⚠️ **Note:** Prottekta file **24 ghonta** por auto-delete hoye jabe!"
        )
        await update.message.reply_text(help_text, parse_mode="Markdown")
        return

    # 2. Jodi key thake (e.g., /start demo ba /start cmbharat)
    key = text[1].lower()
    if key in movies:
        movie_data = movies[key]
        m_name = movie_data.get("name", "File")
        m_lang = movie_data.get("language", "Hindi")
        
        # Files loop (Multiple quality thakle shob pathabe)
        for quality, f_id in movie_data["files"].items():
            caption_text = (
                f"📂 **File:** {m_name}\n"
                f"🔊 **Language:** {m_lang}\n"
                f"💿 **Quality:** {quality}\n\n"
                f"⚠️ **Note:** This file will be auto-deleted in 24 hours!"
            )
            
            try:
                # Ekhane send_document bebohar kora hoyeche jate shob file support kore
                msg = await context.bot.send_document(
                    chat_id=user_id,
                    document=f_id,
                    caption=caption_text,
                    parse_mode="Markdown"
                )
                
                # 24 Hours Timer (86400 seconds)
                context.job_queue.run_once(delete_message, 86400, data=msg.message_id, chat_id=user_id)
                await asyncio.sleep(1) # Spam thekanor jonno
            except Exception as e:
                print(f"Error sending {quality} for {key}: {e}")
    else:
        # Key khunje na pele
        await update.message.reply_text("❌ Sorry, movie/file not found! Please check the link again.")
# Bot Setup
bot_app = ApplicationBuilder().token(TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))

if __name__ == '__main__':
    print("Bot is starting... 🚀")
    bot_app.run_polling()
