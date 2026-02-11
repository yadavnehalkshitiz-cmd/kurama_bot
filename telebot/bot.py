import os
import logging
import re
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import yt_dlp

# --- CONFIGURATION ---
TOKEN = "8540844066:AAEbEf7vH_aKhqTiO_Lx95yH5wR5Oy2Xpmg"  # User provided token
BASE_DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads", "TelegramBot_Videos")

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f"👋 **Hello {user}!**\n\n"
             "I am your personal Video Downloader Assistant.\n"
             "📂 Videos will be saved to: `{BASE_DOWNLOAD_FOLDER}`\n\n"
             "🚀 **Supported Platforms:**\n"
             "• YouTube (Shorts & Videos)\n"
             "• Instagram (Reels & Posts)\n"
             "• TikTok\n"
             "• Facebook\n\n"
             "👇 *Just send me a link to start!*",
        parse_mode='Markdown'
    )

def get_platform_name(url):
    domain = re.search(r'(?:https?://)?(?:www\.)?([^/]+)', url)
    if domain:
        name = domain.group(1).lower()
        if 'youtube' in name or 'youtu.be' in name: return 'YouTube'
        if 'instagram' in name: return 'Instagram'
        if 'tiktok' in name: return 'TikTok'
        if 'facebook' in name or 'fb.watch' in name: return 'Facebook'
        if 'twitter' in name or 'x.com' in name: return 'Twitter'
    return 'Other'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    chat_id = update.effective_chat.id
    
    # Basic URL validation
    if not url.startswith(('http://', 'https://')):
        await context.bot.send_message(chat_id=chat_id, text="⚠️ That doesn't look like a valid link. Please send a URL starting with http:// or https://")
        return

    platform = get_platform_name(url)
    save_folder = os.path.join(BASE_DOWNLOAD_FOLDER, platform)
    
    # Create directory if it doesn't exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Initial status message
    status_msg = await context.bot.send_message(
        chat_id=chat_id, 
        text=f"🔎 **Analyzing link from {platform}...**",
        parse_mode='Markdown'
    )

    # yt-dlp configuration
    ydl_opts = {
        'outtmpl': os.path.join(save_folder, '%(title)s [%(id)s].%(ext)s'),
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Ensure MP4
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'restrictfilenames': True, # ASCII-only filenames
        'ffmpeg_location': os.getcwd(), # Use local ffmpeg
    }

    try:
        # Update status to Downloading
        await context.bot.edit_message_text(
            chat_id=chat_id, 
            message_id=status_msg.message_id, 
            text=f"⬇️ **Downloading from {platform}...**\n_(This might take a moment)_",
            parse_mode='Markdown'
        )
        
        # Run download in a separate thread/process to avoid blocking bot (simplified here)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            video_title = info.get('title', 'Unknown Title')
            
        # Clean up filename for display
        display_path = os.path.abspath(filename)
        
        # Success message
        await context.bot.edit_message_text(
            chat_id=chat_id, 
            message_id=status_msg.message_id, 
            text=f"✅ **Download Complete!**\n\n"
                 f"📺 **Title:** {video_title}\n"
                 f"📂 **Saved to:** `{display_path}`", 
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logging.error(f"Download error: {e}")
        error_text = str(e)
        if "sign in" in error_text.lower():
            nice_error = "This video requires a login (it might be private or age-restricted)."
        else:
            nice_error = f"Could not download the video. Error details: {str(e)}"
            
        await context.bot.edit_message_text(
            chat_id=chat_id, 
            message_id=status_msg.message_id, 
            text=f"❌ **Failed to download**\n\n{nice_error}"
        )

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    
    print(f"Bot is running! Saving files to: {BASE_DOWNLOAD_FOLDER}")
    application.run_polling()
