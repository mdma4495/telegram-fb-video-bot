import telebot
from telebot import types
from config import BOT_TOKEN
from downloader import download_facebook_video
import os

bot = telebot.TeleBot(BOT_TOKEN)

# ----- Keyboard -----
def main_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("📥 Download Video", "ℹ️ Help")
    return kb

# ----- Start -----
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Welcome!\n\nFacebook video link bhejo\nYa button use karo 👇",
        reply_markup=main_keyboard()
    )

# ----- Messages -----
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()

    # Button / keyword handling
    if text in ["📥 download video", "download", "fb", "video"]:
        bot.send_message(
            message.chat.id,
            "📎 Facebook video link bhejo",
            reply_markup=main_keyboard()
        )
        return

    if text in ["ℹ️ help", "help"]:
        bot.send_message(
            message.chat.id,
            "🆘 Help:\n\n1️⃣ Facebook video link bhejo\n2️⃣ Bot video download karke bhej dega",
            reply_markup=main_keyboard()
        )
        return

    # Facebook link check
    if "facebook.com" in text or "fb.watch" in text:
        bot.send_message(message.chat.id, "⏳ Video download ho raha hai...")

        try:
            video_file = download_facebook_video(text)

            with open(video_file, 'rb') as video:
                bot.send_video(message.chat.id, video)

            os.remove(video_file)

        except Exception as e:
            bot.send_message(message.chat.id, "❌ Video download nahi ho paya.")

    else:
        bot.send_message(
            message.chat.id,
            "❗ Galat input\nButton dabao ya Facebook link bhejo",
            reply_markup=main_keyboard()
        )

bot.polling()
