import aiosqlite

DB_NAME = "users.db"

async def init_db():
    """Создание таблицы пользователей, если её нет"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username TEXT,
                joined_at TEXT,
                last_seen TEXT,
                usage_count INTEGER DEFAULT 0
            )
        ''')
        await db.commit()

async def add_user(user_id: int, username: str):
    """Добавляет пользователя в базу данных, если его нет"""
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
        user_exists = await cursor.fetchone()

        if user_exists:
            return

        await db.execute("""
            INSERT INTO users (user_id, username, joined_at, last_seen, usage_count)
            VALUES (?, ?, datetime('now'), datetime('now'), 1)
        """, (user_id, username))
        await db.commit()

async def update_user_activity(user_id: int):
    """Обновляет дату последней активности и увеличивает счётчик"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            UPDATE users
            SET last_seen = datetime('now'),
                usage_count = usage_count + 1
            WHERE user_id = ?
        """, (user_id,))
        await db.commit()

async def get_user_stats(user_id: int):
    """Получает статистику по пользователю"""
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT usage_count, last_seen FROM users WHERE user_id = ?
        """, (user_id,))
        return await cursor.fetchone()
