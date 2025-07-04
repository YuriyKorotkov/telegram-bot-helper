

import asyncio
from aiogram import Bot

TOKEN = "7328447831:AAGs2tFXlPfOsitRYkZjMvUFke--9WVItQY"

async def main():
    bot = Bot(token=TOKEN)
    try:
        user_id = "5203323176"
        message = "Здравствуйте! Спасибо за обратную связь. Всегда рад помочь! Очень приятно что бот вам понравился!)"
        await bot.send_message(chat_id=user_id, text=message)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())





