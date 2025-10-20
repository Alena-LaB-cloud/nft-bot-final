from contextlib import contextmanager
import sqlite3
import types
import  context
from dns.update import Update


@contextmanager
def transaction(connection):
    """Контекстный менеджер для транзакций"""
    try:
        yield connection
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e


async def purchase_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    conn = sqlite3.connect('bot_database.db')

    with transaction(conn):
        cursor = conn.cursor()

        # Получаем цену товара
        cursor.execute("SELECT price FROM items WHERE id = ?", (item_id,))
        price = cursor.fetchone()[0]

        # Проверяем баланс
        cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        balance = cursor.fetchone()[0]

        if balance < price:
            await update.message.reply_text("❌ Недостаточно средств")
            return

        # Списание средств
        cursor.execute(
            "UPDATE users SET balance = balance - ? WHERE user_id = ?",
            (price, user_id)
        )

        # Добавление товара в инвентарь
        cursor.execute(
            "INSERT INTO inventory (user_id, item_id) VALUES (?, ?)",
            (user_id, item_id)
        )

        # Логирование операции
        cursor.execute(
            "INSERT INTO transactions (user_id, type, amount) VALUES (?, 'purchase', ?)",
            (user_id, price)
        )

    await update.message.reply_text("✅ Покупка успешно завершена")

    @contextmanager
    def transaction(connection):
        """Контекстный менеджер для транзакций"""
        try:
            yield connection
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e





    async def purchase_item(update: Update, context: contextmanager(DEFUOLT.type)):
        user_id = update.effective_user.id
        item_id = context.args[0]

        conn = sqlite3.connect('bot_database.db')

        with transaction(conn):
            cursor = conn.cursor()

            # Получаем цену товара
            cursor.execute("SELECT price FROM items WHERE id = ?", (item_id,))
            price = cursor.fetchone()[0]

            # Проверяем баланс
            cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
            balance = cursor.fetchone()[0]

            if balance < price:
                await update.message.reply_text("❌ Недостаточно средств")
                return

            # Списание средств
            cursor.execute(
                "UPDATE users SET balance = balance - ? WHERE user_id = ?",
                (price, user_id)
            )

            # Добавление товара в инвентарь
            cursor.execute(
                "INSERT INTO inventory (user_id, item_id) VALUES (?, ?)",
                (user_id, item_id)
            )

            # Логирование операции
            cursor.execute(
                "INSERT INTO transactions (user_id, type, amount) VALUES (?, 'purchase', ?)",
                (user_id, price)
            )

        await update.message.reply_text("✅ Покупка успешно завершена")