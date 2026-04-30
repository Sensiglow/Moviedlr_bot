import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio

# --- CONFIGURATION ---
ADMIN_ID = 7480551514  # Tomar dewa Admin ID

# --- FLASK SERVER (Keep Alive) ---
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

# --- TELEGRAM BOT TOKEN ---
TOKEN = os.getenv("TOKEN")

# --- MOVIE LIST DATABASE ---
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

# --- FUNCTIONS ---

async def delete_message(context: ContextTypes.DEFAULT_TYPE):
    """24 hours por message delete korbe"""
    job = context.job
    try:
        await context.bot.delete_message(chat_id=job.chat_id, message_id=job.data)
    except Exception as e:
        print(f"Error deleting: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handle korbe"""
    if not update.message or not update.message.text:
        return

    user_id = update.effective_user.id
    text = update.message.text.split()
    
    # User jodi sudhu /start likhe
    if len(text) == 1:
        help_text = (
            "👋 **Welcome to the Download Bot!**\n\n"
            "Ami apnake Movie download korte sahajyo kori। Movie pete channel-er link-e click korun, "
            "ba `/start moviename` (e.g. `/start demo`) likhe send korun।\n\n"
            "⚠️ **Note:** Prottekta movie **24 ghonta** por auto-delete hoye jabe!"
        )
        await update.message.reply_text(help_text, parse_mode="Markdown")
        return

    # Movie link process kora
    key = text[1].lower()
    if key in movies:
        movie_data = movies[key]
        m_name = movie_data.get("name", "File")
        m_lang = movie_data.get("language", "Hindi")
        
        for quality, f_id in movie_data["files"].items():
            caption_text = (
                f"🎬 **Movie:** {m_name}\n"
                f"🔊 **Language:** {m_lang}\n"
                f"💿 **Quality:** {quality}\n\n"
                f"⚠️ **Note:** This video will be auto-deleted in 24 hours!"
            )
            try:
                msg = await context.bot.send_video(
                    chat_id=user_id,
                    video=f_id,
                    caption=caption_text,
                    parse_mode="Markdown"
                )
                
                # 24 Hours Timer (86400 seconds)
                context.job_queue.run_once(delete_message, 86400, data=msg.message_id, chat_id=user_id)
                await asyncio.sleep(1) 
            except Exception as e:
                print(f"Error sending: {e}")
    else:
        await update.message.reply_text("❌ Sorry, movie not found!")

async def handle_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin video pathale File ID ber kore debe"""
    if update.effective_user.id == ADMIN_ID:
        if update.message.video:
            f_id = update.message.video.file_id
        elif update.message.document:
            f_id = update.message.document.file_id
        else:
            return

        await update.message.reply_text(
            f"✅ **Admin, your File ID:**\n\n`{f_id}`\n\n👆 Click to copy",
            parse_mode="Markdown"
        )

# --- BOT APP BUILD ---
bot_app = ApplicationBuilder().token(TOKEN).build()

bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(MessageHandler(filters.VIDEO | filters.Document.ALL, handle_files))

if __name__ == '__main__':
    print("Bot is starting... 🚀")
    bot_app.run_polling()
