import sqlite3
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def init_database():
    """Инициализация базы данных"""
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    cursor = conn.cursor()

    # Таблица пользователей с кошельками
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            wallet_address TEXT UNIQUE,
            balance REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Таблица NFT
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nfts (
            nft_id TEXT PRIMARY KEY,
            user_id INTEGER,
            name TEXT,
            description TEXT,
            image_path TEXT,
            price_ton REAL DEFAULT 0.0,
            for_sale BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')

    conn.commit()
    conn.close()
    logger.info("✅ Database initialized")


def save_wallet_address(user_id: int, username: str, wallet_address: str) -> bool:
    """Сохраняет адрес кошелька в БД"""
    try:
        conn = sqlite3.connect('bot_database.db', check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, username, wallet_address)
            VALUES (?, ?, ?)
        ''', (user_id, username, wallet_address))

        conn.commit()

        # Проверим, что запись сохранилась
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        logger.info(f"✅ Wallet saved for user {user_id}: {wallet_address}")
        logger.info(f"📋 Database record: {result}")

        conn.close()
        return True

    except sqlite3.IntegrityError:
        logger.error(f"❌ Wallet address already exists: {wallet_address}")
        return False
    except Exception as e:
        logger.error(f"❌ Error saving wallet: {e}")
        return False

def get_wallet_address(user_id: int) -> Optional[str]:
    """Получает адрес кошелька из БД"""
    try:
        conn = sqlite3.connect('bot_database.db', check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT wallet_address FROM users WHERE user_id = ?
        ''', (user_id,))

        result = cursor.fetchone()
        conn.close()

        return result[0] if result else None

    except Exception as e:
        logger.error(f"❌ Error getting wallet: {e}")
        return None


def user_has_wallet(user_id: int) -> bool:
    """Проверяет, есть ли у пользователя кошелек"""
    return get_wallet_address(user_id) is not None

