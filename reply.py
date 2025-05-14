

import asyncio
from aiogram import Bot

TOKEN = "YOUR_TOKEN"

async def main():
    bot = Bot(token=TOKEN)
    try:
        user_id = "YOUR_ID"
        message = "Здравствуйте, Светлана! Спасибо за обращение. В главном меню перейдите в раздел <<Инструкции для заказщика>> далее в подменю нажмите на <<Добавление фото>> и бот пришлет вам инструкцию"
        await bot.send_message(chat_id=user_id, text=message)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())





