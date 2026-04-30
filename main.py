import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio

# --- CONFIGURATION ---
ADMIN_ID = 123456789  # <--- EKHANE TOMAR ADMIN ID BOSHAO (Example: 54321678)

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

# --- TELEGRAM BOT SETTINGS ---
TOKEN = os.getenv("TOKEN")

# --- MOVIE LIST ---
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
            "480p": "BAACAgUAAxkBAAFId2Bp_GofnK_v7X_N6Gz0_0S7Y7n6AAI8HwAC_MWRV_pU8-P_zXpROwE",
            "720p": "BAACAgUAAxkBAAFId2Np_GogY8N7O9G9_S3Y7n6AAI9HwAC_MWRV-P_zXpROwE",
            "1080p": "BAACAgUAAxkBAAFId2Vp_GohY8N7O9G9_S3Y7n6AAI-HwAC_MWRV-P_zXpROwE"
        }
    }
}

# --- FUNCTIONS ---

async def delete_message(context: ContextTypes.DEFAULT_TYPE):
    """Timer shesh hole message delete korbe"""
    job = context.job
    try:
        await context.bot.delete_message(chat_id=job.chat_id, message_id=job.data)
    except Exception as e:
        print(f"Error deleting: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handle korbe (Movie pathabe)"""
    if not update.message or not update.message.text:
        return

    user_id = update.effective_user.id
    text = update.message.text.split()
    
    if len(text) > 1:
        key = text[1].lower()
        if key in movies:
            movie_data = movies[key]
            m_name = movie_data.get("name", "Unknown")
            m_lang = movie_data.get("language", "Hindi")
            
            for quality, f_id in movie_data["files"].items():
                caption_text = (
                    f"🎬 **Movie:** {m_name}\n"
                    f"🔊 **Language:** {m_lang}\n"
                    f"💿 **Quality:** {quality}\n\n"
                    f"⚠️ **Note:** Video will be auto-deleted in 24 hours!"
                )
                
                try:
                    msg = await context.bot.send_video(
                        chat_id=user_id,
                        video=f_id,
                        caption=caption_text,
                        parse_mode="Markdown"
                    )
                    # 24 hours timer (86400 seconds)
                    context.job_queue.run_once(delete_message, 86400, data=msg.message_id, chat_id=user_id)
                    await asyncio.sleep(1)
                except Exception as e:
                    print(f"Error: {e}")
        else:
            await update.message.reply_text("Movie not found ❌")

async def handle_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin video pathale File ID ber kore debe"""
    user_id = update.effective_user.id
    
    # Shudhu tumi (Admin) holei ID pabe
    if user_id == ADMIN_ID:
        if update.message.video:
            f_id = update.message.video.file_id
        elif update.message.document:
            f_id = update.message.document.file_id
        else:
            return

        await update.message.reply_text(
            f"✅ **Admin, your File ID:**\n\n`{f_id}`\n\n👆 Click to copy and use in movies list.",
            parse_mode="Markdown"
        )
    # Shadharon user-ra video pathale bot ignore korbe

# --- APP BUILD ---
bot_app = ApplicationBuilder().token(TOKEN).build()

bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(MessageHandler(filters.VIDEO | filters.Document.ALL, handle_files))

if __name__ == '__main__':
    print("Bot is starting... 🚀")
    bot_app.run_polling()
