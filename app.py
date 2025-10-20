from flask import Flask
import os
from threading import Thread
from telebot import TeleBot
import time

app = Flask(__name__)
bot = TeleBot('8429039115:AAFLkJFjhgbpMyva7Kf5fHydDOVIPWdRCdc')

@app.route('/')
def home():
    return "✅ Bot Server Running!"

@app.route('/health')
def health():
    return "OK"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot is online!")

def bot_polling():
    print("🤖 Bot started in background")
    while True:
        try:
            bot.infinity_polling()
        except Exception as e:
            print(f"Bot error, restarting: {e}")
            time.sleep(5)

# Запускаем бот в фоне
Thread(target=bot_polling, daemon=True).start()

# Запускаем веб-сервер
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Web server starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
