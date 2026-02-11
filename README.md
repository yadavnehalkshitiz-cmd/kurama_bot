Supported platforms:

✅ YouTube (Videos & Shorts)
✅ Instagram (Reels & Posts)
✅ TikTok
✅ Facebook
✅ Twitter / X

🚀 Features

Simple: just send a video link to the bot

Auto-detects platform (YouTube, Instagram, TikTok, etc.)

Downloads best available MP4 quality

Organizes downloads by platform

Shows download status in Telegram

Uses yt-dlp for powerful extraction

Videos are saved to:

~/Downloads/TelegramBot_Videos/


(with subfolders per platform)

📦 Requirements

Make sure you have:

Python 3.10+

FFmpeg installed

Telegram Bot Token

Internet connection 😄

Install Python packages:
pip install python-telegram-bot yt-dlp

🔧 FFmpeg Setup
Windows

Download FFmpeg:
https://ffmpeg.org/download.html

Extract it.

Add FFmpeg to PATH
(or place ffmpeg.exe in your project folder).

Check:

ffmpeg -version

Linux
sudo apt install ffmpeg

🤖 Create Telegram Bot

Open Telegram

Search @BotFather

Run:

/start
/newbot


Copy your BOT TOKEN

Replace this line in code:

TOKEN = "YOUR_TOKEN_HERE"

▶️ Run the Bot

From your project directory:

python bot.py


You should see:

Bot is running! Saving files to: ...


Now open Telegram and send /start to your bot.

💬 Usage

Start bot:

/start


Paste any supported video link.

Example:

https://www.youtube.com/watch?v=xxxx


Bot will:

🔎 Analyze
⬇️ Download
✅ Save locally

📁 Folder Structure
TelegramBot_Videos/
│
├── YouTube/
├── Instagram/
├── TikTok/
├── Facebook/
└── Twitter/

⚠️ Notes

Private / age-restricted videos may fail.

Very long videos may take time.
by ak

Filename is sanitized automatically.

This bot downloads to YOUR PC (not cloud).
