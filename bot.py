import telebot
from config import BOT_TOKEN
from downloader import download_facebook_video
import os

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "👋 Welcome!\n\nFacebook video link bhejo,\nmain video download karke bhej dunga 📥"
    )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text

    if "facebook.com" in url or "fb.watch" in url:
        bot.reply_to(message, "⏳ Video download ho raha hai, wait karo...")

        try:
            video_file = download_facebook_video(url)

            with open(video_file, 'rb') as video:
                bot.send_video(message.chat.id, video)

            os.remove(video_file)

        except:
            bot.reply_to(message, "❌ Video download nahi ho paya.")

    else:
        bot.reply_to(message, "❗ Sirf Facebook video link bhejo.")

bot.polling()
