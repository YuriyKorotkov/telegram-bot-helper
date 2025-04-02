import asyncio
from aiogram import Bot
from aiogram.types import InputFile
from database import get_all_users  # Импортируем функцию получения всех пользователей
from config import TOKEN  # Токен для подключения к боту

import os

bot = Bot(token=TOKEN)
image_path = "images/Group 1.jpg"

async def send_image_to_all_users(image_path: str, caption: str):
    """Отправляет заранее подготовленную картинку всем пользователям с текстом"""
    user_ids = await get_all_users()  # Получаем всех пользователей из БД
    for user_id in user_ids:
        try:
            with open(image_path, 'rb') as image_file:
                await bot.send_photo(user_id, InputFile(image_file), caption=caption)
        except Exception as e:
            print(f"Не удалось отправить картинку пользователю {user_id}: {e}")

async def main():
    # Указываем путь до картинки и текст, который будет в подписи
    image_path = "path_to_your_image.png"  # Путь до заранее подготовленной картинки
    caption = "Это заранее подготовленная картинка с подписью!"  # Текст для подписи

    await send_image_to_all_users(image_path, caption)  # Отправляем картинку всем пользователям

if __name__ == "__main__":
    asyncio.run(main())  # Запускаем основную функцию

