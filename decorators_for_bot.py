from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from functools import wraps
import logging
import os

BASE_DIR = os.getcwd()
file_attachments = {
    "add_object": os.path.join(BASE_DIR, "files", "Шаблон импорта данных по объектам.xlsx"),
    "instruction_schedule": os.path.join(BASE_DIR, "files", "Презентация  Календарно-сетевой график___.pdf"),
    "add_user": os.path.join(BASE_DIR, "files", "Шаблон на предоставление доступа пользователям.xlsx"),
    "tim1": os.path.join(BASE_DIR, "files", "Отчет_по_ТИМ_бывш_отчет_ЦКС_инструкция_—_11_07_24.pdf"),
    "tim2": os.path.join(BASE_DIR, "files", "Добавление требований к ТИМ и ЦИМ в объект.pdf"),
    "road": os.path.join(BASE_DIR, "files", "Добавление фотоотчета в объект.pdf"),
    "dock_1": os.path.join(BASE_DIR, "files", "Добавление документов в объект.pdf"),
    "vis_1": os.path.join(BASE_DIR, "files", "Шаблон заявки для ввода.xlsx"),
    "vis_2": os.path.join(BASE_DIR, "files",  "Инструкция по заполнению интеграционной формы.pdf"),
    "object_card_1": os.path.join(BASE_DIR, "files",  "Презентация работа с карточкой объекта.pdf"),
    "electron1": os.path.join(BASE_DIR, "images", "electron.png"),
    "construction_control11": os.path.join(BASE_DIR, "files", "Строительный контроль в модуле заказчика.pdf"),
    "upload_pd_rd11": os.path.join(BASE_DIR, "files", "Инструкция по загрузке ПД и РД в модуле заказчика.pdf"),
    "sign_participants11": os.path.join(BASE_DIR, "files", "Прикрепление приказов и подписи в проектах.pdf"),
    "exchange_docs11": os.path.join(BASE_DIR, "files", "Обмен исполнительной документацией.pdf"),

}

# 📌 Декоратор для обработки ошибок
def catch_exceptions(default_message="⚠️ Произошла ошибка, попробуйте позже."):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logging.error(f"Ошибка в {func.__name__}: {e}")
                call = args[0]
                await call.message.answer(default_message)
        return wrapper
    return decorator


def check_file_exists(file_key):
    def decorator(func):
        @wraps(func)
        async def wrapper(call: CallbackQuery, *args, **kwargs):
            file_path = file_attachments.get(file_key)
            if not file_path:
                await call.message.answer("⚠️ Файл не найден. Обратитесь к администратору.")
                return
            return await func(call, file_path, *args, **kwargs)
        return wrapper
    return decorator



def show_progress(total_steps=10, step_delay=0.1):
    """Декоратор, который запускает основную задачу параллельно с прогресс-баром."""

    def decorator(func):
        @wraps(func)
        async def wrapper(call: CallbackQuery, *args, **kwargs):
            spinner = ["⏳", "⌛"]
            progress_message = await call.message.answer(
                f"{spinner[0]} Загрузка...",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="⬛" * total_steps + " Загрузка... 0%", callback_data="loading")]
                ])
            )

            # Запускаем основную функцию в фоне
            task = asyncio.create_task(func(call, *args, **kwargs))

            # Показываем прогресс, пока основная функция выполняется
            for i in range(1, total_steps + 1):
                await asyncio.sleep(step_delay)
                progress_percent = i * (100 // total_steps)
                filled_blocks = "🟩" * i
                empty_blocks = "⬛" * (total_steps - i)
                progress_bar = filled_blocks + empty_blocks
                current_spinner = spinner[i % 2]

                await progress_message.edit_text(
                    f"{current_spinner} Загрузка...",
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text=f"{progress_bar} Загрузка... {progress_percent}%",
                                              callback_data="loading")]
                    ])
                )

                # Если файл уже отправился — выходим из цикла
                if task.done():
                    break

            await task  # Дожидаемся завершения основной функции
            await progress_message.delete()  # Удаляем прогресс-бар

        return wrapper

    return decorator

