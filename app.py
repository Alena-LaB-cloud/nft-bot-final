from flask import Flask
import os
import threading
import asyncio
import logging
from dbm import sqlite3
from telebot import TeleBot, types
from telebot.types import Message, CallbackQuery
import tempfile

# Импортируйте ваши модули
from config import ADMIN_IDS, MIN_NFT_PRICE, MAX_NFT_PRICE
from ton_connector import TonConnect
from ton_manager import ton_manager
from nft_creator import NFTCreator
from DataBase import init_database, save_wallet_address, get_wallet_address

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация Flask
app = Flask(__name__)

# Инициализация бота
bot = TeleBot('8429039115:AAFLkJFjhgbpMyva7Kf5fHydDOVIPWdRCdc')
nft_creator = NFTCreator()

# Состояния пользователей
user_states = {}

class UserState:
    def __init__(self):
        self.waiting_for = None
        self.data = {}

def get_user_state(user_id: int) -> UserState:
    if user_id not in user_states:
        user_states[user_id] = UserState()
    return user_states[user_id]

# Ваши команды бота (добавьте сюда весь ваш код команд)
@bot.message_handler(commands=['start'])
def start_command(message: Message):
    user = message.from_user
    welcome_text = f"🎨 Привет, {user.first_name}!\n\nЯ NFT бот для TON сети!"
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(commands=['status'])
def status_command(message: Message):
    bot.reply_to(message, "✅ Бот работает на Render!")

# Добавьте сюда ВСЕ остальные ваши команды и обработчики...

# Flask routes
@app.route('/')
def home():
    return "🤖 NFT Telegram Bot is running on Render!"

@app.route('/health')
def health():
    return "OK"

@app.route('/stats')
def stats():
    return f"Active users: {len(user_states)}"

def run_bot():
    """Запуск бота в отдельном потоке"""
    try:
        logger.info("🤖 Starting Telegram bot...")
        
        # Инициализация базы данных
        init_database()
        
        # Инициализация TON провайдера
        asyncio.run(ton_manager.init_provider())
        
        logger.info("✅ Bot initialized, starting polling...")
        bot.infinity_polling()
        
    except Exception as e:
        logger.error(f"❌ Bot error: {e}")

if __name__ == "__main__":
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Запускаем веб-сервер
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"🚀 Starting web server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
    
