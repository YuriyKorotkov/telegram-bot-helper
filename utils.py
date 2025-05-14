import os
import sys
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
)
sys.path.append(os.path.join(os.path.dirname(__file__), 'text1.py'))
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💡 Что такое ИСУП? / НПА 📑", callback_data="menu:about_isup")],
        [InlineKeyboardButton(text="🛠️ Добавление объекта/пользователя", callback_data="menu:add_object_user")],
        [InlineKeyboardButton(text="📝 Инструкции для заказчика", callback_data="menu:instruction_schedule")],
        [InlineKeyboardButton(text="📲 Подписаться на каналы", callback_data="menu:subscribe")],
        [InlineKeyboardButton(text="📧 Форма обратной связи", callback_data="menu:feedback")],
    ])

def get_back_button():
    return InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")

async def return_to_main_menu(call: CallbackQuery, state: FSMContext, menu_key: str = None):
    """Функция возвращает пользователя на предыдущий уровень или в главное меню."""
    data = await state.get_data()
    previous_menu = menu_key or data.get("previous_menu")

    # Карта меню и клавиатур
    menu_mapping = {
        "menu:add_object_user": "⬇️ Добавление объекта/пользователя:",
        "menu:about_isup": "⬇️ Что такое ИСУП? / НПА: ⬇️",
        "menu:instruction_schedule": "⬇️ Инструкции для заказчика: ⬇️",
        "menu:integration_vis": "⬇️ Интеграция ВИС ⬇️",
        "menu:customer_module": "⬇️  Модуль заказчика ⬇️",
        "menu:fill_tim_report": "⬇️  Раздел 'Отчет ТИМ'⬇️",
    }

    keyboard_mapping = {
        "menu:add_object_user": InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👤 Добавить пользователя", callback_data="submenu:add_user")],
            [InlineKeyboardButton(text="🏢 Добавить объект", callback_data="submenu:add_object")],
            [InlineKeyboardButton(text="🔑 Забыли пароль?", callback_data="submenu:forgot_password")],
            [InlineKeyboardButton(text="🚫 Блокировка пользователя", callback_data="submenu:block_user")],
            [InlineKeyboardButton(text="🔙 В главное меню", callback_data="menu:back_to_main7")]
        ]),
        "menu:about_isup": InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🌟 Преимущества использования ИСУП", callback_data="submenu:advantages")],
            [InlineKeyboardButton(text="📄 Документы НПА", callback_data="submenu:documents")],
            [InlineKeyboardButton(text="ℹ️ Справочная информация", callback_data="submenu:info")],
            [InlineKeyboardButton(text="🔙 В главное меню", callback_data="menu:back_to_main7")]
        ]),
        "menu:instruction_schedule": InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏢 Заполнение карточки объекта", callback_data="submenu:fill_object_card")],
            [InlineKeyboardButton(text="📅 Календарно-сетевой график", callback_data="submenu:keg")],
            [InlineKeyboardButton(text="🖼️ Добавление фото", callback_data="submenu:add_photo_docs")],
            [InlineKeyboardButton(text="📝 Добавление документации", callback_data="submenu:add_docs")],
            [InlineKeyboardButton(text="📊 Заполнение данных для отчета ТИМ", callback_data="submenu:fill_tim_report")],
            [InlineKeyboardButton(text="📞 Обращение в техподдержку", callback_data="submenu:tech_support")],
            [InlineKeyboardButton(text="🧑‍💼 Модуль заказчика", callback_data="submenu:customer_module")],
            [InlineKeyboardButton(text="🔙 В главное меню", callback_data="menu:back_to_main7")]
        ]),
        "menu:integration_vis": InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📅 Шаблон заявки для ввода", callback_data="submenu:add_vis_1")],
            [InlineKeyboardButton(text="➕ Инструкция по заполнению интеграционной формы", callback_data="submenu:add_vis_2")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="menu:customer_module")]
        ]),
        "menu:fill_tim_report": InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📊 Заполнение данных для отчета ТИМ", callback_data="submenu:fill_tim_data")],
            [InlineKeyboardButton(text="➕ Добавление требований к ТИМ и ЦИМ-модели",
                                  callback_data="submenu:add_tim_requirements")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="menu:instruction_schedule")]
        ]),

        "menu:customer_module": InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Первичная интеграция с ВИС", callback_data="submenu:integration_vis")],
            [InlineKeyboardButton(text="🖊️ Выпуск ЭЦП и МЧД для пользователя", callback_data="submenu:issue_digital_signature")],
            [InlineKeyboardButton(text="📝 Подписание участников", callback_data="submenu:sign_participants")],
            [InlineKeyboardButton(text="📤 Загрузка ПД/РД и передача в производство", callback_data="submenu:upload_pd_rd")],
            [InlineKeyboardButton(text="📑 Обмен исполнительной документацией", callback_data="submenu:exchange_docs")],
            [InlineKeyboardButton(text="🧑‍⚖️ Строительный контроль в модуле заказчика", callback_data="submenu:construction_control")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="menu:instruction_schedule")]
        ])
    }

    if previous_menu and previous_menu in menu_mapping:
        try:
            await call.message.delete()  # Удаляем старое сообщение
            await call.message.answer(
                menu_mapping[previous_menu],
                reply_markup=keyboard_mapping.get(previous_menu, main_menu())  # Отправляем новое сообщение с клавиатурой
            )
            await state.update_data(previous_menu=previous_menu)  # Сохраняем текущее меню для кнопки назад
            return
        except Exception as e:
            logging.warning(f"Ошибка при редактировании сообщения: {e}")

    # Если previous_menu отсутствует или произошла ошибка, отправляем пользователя в главное меню
    await state.clear()
    try:
        await call.message.delete()  # Удаляем старое сообщение
        # Удаление сообщения с обратной связью (опционально)
        # if data.get("feedback_msg_id"):
        #     await bot.delete_message(call.message.chat.id, data["feedback_msg_id"])
    except Exception as e:
        logging.warning(f"Ошибка при удалении сообщений: {e}")

    try:
        await call.message.answer("Главное меню:", reply_markup=main_menu())
    except Exception as e:
        logging.error(f"Ошибка при отправке главного меню: {e}")



async def return_to_main_menu7(call: CallbackQuery, state: FSMContext):
    """Функция для возврата пользователя в главное меню."""
    # Очистить состояние пользователя
    await state.clear()

    # Удаляем текущее сообщение
    try:
        await call.message.delete()
    except Exception as e:
        logging.warning(f"Ошибка при удалении сообщения: {e}")

    # Отправляем сообщение с главным меню
    try:
        await call.message.answer("Главное меню:", reply_markup=main_menu())
    except Exception as e:
        logging.error(f"Ошибка при отправке главного меню: {e}")

