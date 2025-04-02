import aiosqlite

from send_info import bot

DB_NAME = "users.db"


async def init_db():
    """Создание таблицы пользователей, если её нет"""
    print("Инициализация базы данных...")  # Отладка
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username TEXT
            )
        ''')
        await db.commit()


async def add_user(user_id: int, username: str):
    """Добавляет пользователя в базу данных"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO users (user_id, username) 
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET username=excluded.username
        """, (user_id, username))
        await db.commit()

async def get_all_users():
    """Получить всех пользователей из базы данных"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT user_id FROM users") as cursor:
            users = await cursor.fetchall()
            return [user[0] for user in users]  # Извлекаем только user_id


async def send_message_to_all_users(message_text: str):
    """Отправить сообщение всем пользователям"""
    user_ids = await get_all_users()  # Получаем всех пользователей
    for user_id in user_ids:
        try:
            await bot.send_message(user_id, message_text)  # Отправляем сообщение
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")


