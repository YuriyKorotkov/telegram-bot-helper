import os
import sys
from aiogram import F
import asyncio
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, FSInputFile
)
from aiogram.filters import CommandStart
from decorators_for_bot import show_progress, catch_exceptions, check_file_exists,file_attachments
# Подключаем файл с текстовыми ответами
sys.path.append(os.path.join(os.path.dirname(__file__), 'text1.py'))
from text1 import text_answers
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

ADMIN_IDS = [1316342598]

TOKEN = "7328447831:AAGQ7ncM4WSfLrgxOomkjRH5Azy-mYipVgk"

bot = Bot(token=TOKEN)
dp = Dispatcher()

class Feedback(StatesGroup):
    waiting_for_message = State()


logging.basicConfig(level=logging.INFO)


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

@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer(
        "👋 Привет! 🤖\n"
        "Это чат-бот Краснодарского края для автоматизации работы заказчиков в ИСУП 🏗️\n\n"
        "<a href='https://t.me/+ObD-6zTF1ngzNjgy'>🔗 Подписаться на рабочий чат</a>",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

@dp.callback_query()
async def menu_handler(call: CallbackQuery, state: FSMContext):
    try:
        if call.data == "menu:feedback":
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="🔙 В главное меню", callback_data="menu:back_to_main7")]]
            )

            try:
                await call.message.delete()  # Удаляем предыдущее сообщение
            except Exception as e:
                logging.warning(f"Не удалось удалить сообщение: {e}")

            await bot.send_message(
                call.message.chat.id,
                "✍️ Пожалуйста,\n введите ваше сообщение\n для отправки администратору:",
                reply_markup=keyboard
            )
            await state.set_state(Feedback.waiting_for_message)

        elif call.data == "menu:add_object_user":
            await state.update_data(previous_menu="menu:add_object_user")  # Сохраняем текущее меню
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="👤 Добавить пользователя", callback_data="submenu:add_user")],
                [InlineKeyboardButton(text="🏢 Добавить объект", callback_data="submenu:add_object")],
                [InlineKeyboardButton(text="🔑 Забыли пароль?", callback_data="submenu:forgot_password")],
                [InlineKeyboardButton(text="🚫 Блокировка пользователя", callback_data="submenu:block_user")],
                [InlineKeyboardButton(text="🔙 В главное меню", callback_data="menu:back_to_main7")]
            ])
            await call.message.edit_text("⬇️Добавление объекта/пользователя:", reply_markup=keyboard)

        elif call.data == "menu:about_isup":
            await state.update_data(previous_menu="menu:about_isup")  # Сохраняем текущее меню
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🌟 Преимущества использования ИСУП", callback_data="submenu:advantages")],
                [InlineKeyboardButton(text="📄 Документы НПА", callback_data="submenu:documents")],
                [InlineKeyboardButton(text="ℹ️ Справочная информация", callback_data="submenu:info")],
                [InlineKeyboardButton(text="🔙 В главное меню", callback_data="menu:back_to_main7")]
            ])
            await call.message.edit_text("⬇️ Что такое ИСУП? / НПА: ⬇️", reply_markup=keyboard)

        elif call.data == "submenu:advantages":
            await state.update_data(previous_menu="menu:about_isup")  # Сохраняем текущее меню
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")]
            ])
            await call.message.edit_text(
                text_answers["what_is_isup"],
                reply_markup=keyboard,
                parse_mode="HTML"
            )

        elif call.data == "menu:instruction_schedule":
            await state.update_data(previous_menu="menu:instruction_schedule")  # Сохраняем текущее меню
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🏢 Заполнение карточки объекта", callback_data="submenu:fill_object_card")],
                [InlineKeyboardButton(text="📅 Календарно-сетевой график", callback_data="submenu:keg")],
                [InlineKeyboardButton(text="🖼️ Добавление фото", callback_data="submenu:add_photo_docs")],
                [InlineKeyboardButton(text="📝 Добавление документации", callback_data="submenu:add_docs")],
                [InlineKeyboardButton(text="📊 Заполнение данных для отчета ТИМ", callback_data="submenu:fill_tim_report")],
                [InlineKeyboardButton(text="📞 Обращение в техподдержку", callback_data="submenu:tech_support")],
                [InlineKeyboardButton(text="🧑‍💼 Модуль заказчика", callback_data="submenu:customer_module")],
                [InlineKeyboardButton(text="🔙 В главное меню", callback_data="menu:back_to_main7")]
            ])
            await call.message.edit_text("⬇️ Инструкции для заказчика: ⬇️", reply_markup=keyboard)

        elif call.data == "submenu:customer_module":
            await state.update_data(previous_menu="menu:customer_module")
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔗 Первичная интеграция с ВИС", callback_data="submenu:integration_vis")],
                [InlineKeyboardButton(text="🖊️ Выпуск ЭЦП и МЧД для пользователя", callback_data="submenu:issue_digital_signature")],
                [InlineKeyboardButton(text="📝 Подписание участников", callback_data="submenu:sign_participants")],
                [InlineKeyboardButton(text="📤 Загрузка ПД/РД и передача в производство", callback_data="submenu:upload_pd_rd")],
                [InlineKeyboardButton(text="📑 Обмен исполнительной документацией", callback_data="submenu:exchange_docs")],
                [InlineKeyboardButton(text="🧑‍⚖️ Строительный контроль в модуле заказщика", callback_data="submenu:construction_control")],
                [InlineKeyboardButton(text="🔙 Назад", callback_data="menu:instruction_schedule")]
            ])
            await call.message.edit_text("📂 Раздел 'Модуль заказчика':⬇️", reply_markup=keyboard)

        elif call.data == "submenu:fill_tim_report":
            await state.update_data(previous_menu="menu:instruction_schedule")  # Сохраняем текущее меню
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📊 Заполнение данных для отчета ТИМ",
                                      callback_data="submenu:fill_tim_data")],
                [InlineKeyboardButton(text="➕ Добавление требований к ТИМ и ЦИМ-модели",
                                      callback_data="submenu:add_tim_requirements")],
                [InlineKeyboardButton(text="🔙 Назад", callback_data="menu:instruction_schedule")]
            ])
            await call.message.edit_text(text="📂 Раздел 'Отчет ТИМ':⬇️", reply_markup=keyboard)

        elif call.data == "submenu:fill_tim_data":
            await state.update_data(previous_menu="menu:fill_tim_report")  # Сохраняем текущее меню
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад", callback_data="submenu:fill_tim_report")]
            ])
            await add_tim_1(call)

        elif call.data == "submenu:add_tim_requirements":
            await state.update_data(previous_menu="submenu:fill_tim_report")  # Сохраняем текущее меню
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад", callback_data="submenu:fill_tim_report")]
            ])
            await add_tim_2(call)

        elif call.data == "submenu:integration_vis":
            await state.update_data(previous_menu="menu:instruction_schedule")  # Сохраняем текущее меню
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📅 Шаблон заявки для ввода",
                                      callback_data="submenu:add_vis_1")],
                [InlineKeyboardButton(text="➕ Инструкция по заполнению интеграционной формы",
                                      callback_data="submenu:add_vis_2")],
                [InlineKeyboardButton(text="🔙 Назад", callback_data="menu:instruction_schedule")]
            ])
            await call.message.edit_text(text_answers["instruction_text"], reply_markup=keyboard)

        elif call.data == "submenu:add_vis_1":
            await state.update_data(previous_menu="submenu:integration_vis")  # Сохраняем текущее меню
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад", callback_data="submenu:integration_vis")]
            ])
            await add_vis_11(call)

        elif call.data == "submenu:add_vis_2":
            await state.update_data(previous_menu="submenu:integration_vis")  # Сохраняем текущее меню
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад", callback_data="submenu:integration_vis")]
            ])
            await add_vis_22(call)

        elif call.data == "submenu:add_object":
            await send_add_object_file(call)

        elif call.data == "submenu:forgot_password":
            await forgot_password_handler(call)

        elif call.data == "submenu:keg":
            await send_keg_instruction(call)

        elif call.data == "menu:back":
            await back_to_previous_menu(call, state)  # Возврат в предыдущее меню

        elif call.data == "menu:back_to_main7":
            # Вызовем функцию для возврата в главное меню
            await return_to_main_menu7(call, state)

        elif call.data == "submenu:add_user":
            await state.update_data(previous_menu="menu:add_object_user")
            await send_add_user_file(call)

        elif call.data == "menu:subscribe":
            await send_subscription_links(call)

        elif call.data == "submenu:documents":
            await send_documents_link(call)

        elif call.data == "submenu:issue_digital_signature":
            await issue_digital_signature(call)

        elif call.data == "submenu:info":
            await info1(call)

        elif call.data == "submenu:add_photo_docs":
            await send_road(call)

        elif call.data == "submenu:add_docs":
            await add_dock_1(call)

        elif call.data == "submenu:fill_object_card":
            await object_card(call)

        elif call.data == "submenu:construction_control":
            await construction_control1(call)

        elif call.data == "submenu:sign_participants":
            await sign_participants1(call)

        elif call.data == "submenu:upload_pd_rd":
            await upload_pd_rd1(call)

        elif call.data == "submenu:exchange_docs":
            await exchange_docs1(call)

        elif call.data == "submenu:block_user":
            await block_user1(call)

        await call.answer()

    except Exception as e:
        logging.error(f"Ошибка обработки callback: {e}")
        await call.answer("Произошла ошибка. Попробуйте снова.", show_alert=True)



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
        if data.get("feedback_msg_id"):
            await bot.delete_message(call.message.chat.id, data["feedback_msg_id"])
    except Exception as e:
        logging.warning(f"Ошибка при удалении сообщений: {e}")

    try:
        await call.message.answer("Главное меню:", reply_markup=main_menu())
    except Exception as e:
        logging.error(f"Ошибка при отправке главного меню: {e}")


@dp.callback_query(F.data == "menu:back")
async def back_to_previous_menu(call: CallbackQuery, state: FSMContext):
    """Обработчик кнопки 'Назад'."""
    await return_to_main_menu(call, state)

@dp.callback_query(F.data == "menu:customer_module")
async def show_customer_module(call: CallbackQuery, state: FSMContext):
    """Обработчик для кнопки возвращения в модуль заказчика."""
    await return_to_main_menu(call, state, "menu:customer_module")


@show_progress(total_steps=5, step_delay=0.05)
@catch_exceptions()
@check_file_exists('exchange_docs11')
async def exchange_docs1(call: CallbackQuery, file_path: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")]]
    )

    doc = FSInputFile(file_path)
    await call.message.delete()

    await call.bot.send_document(
        chat_id=call.message.chat.id,
        document=doc,
        caption="⬆️ Нажмите, чтобы скачать и изучить методические материалы📄",
        reply_markup=keyboard
    )


@show_progress(total_steps=5, step_delay=0.05)
@catch_exceptions()
@check_file_exists('sign_participants11')
async def sign_participants1(call: CallbackQuery, file_path: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")]]
    )

    doc = FSInputFile(file_path)
    await call.message.delete()

    await call.bot.send_document(
        chat_id=call.message.chat.id,
        document=doc,
        caption="⬆️ Нажмите, чтобы скачать и изучить методические материалы📄",
        reply_markup=keyboard
    )


@show_progress(total_steps=5, step_delay=0.05)
@catch_exceptions()
@check_file_exists('upload_pd_rd11')
async def upload_pd_rd1(call: CallbackQuery, file_path: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")]]
    )

    doc = FSInputFile(file_path)
    await call.message.delete()

    await call.bot.send_document(
        chat_id=call.message.chat.id,
        document=doc,
        caption="⬆️ Нажмите, чтобы скачать и изучить методические материалы📄",
        reply_markup=keyboard
    )


@show_progress(total_steps=5, step_delay=0.05)
@catch_exceptions()
@check_file_exists('construction_control11')
async def construction_control1(call: CallbackQuery, file_path: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")]]
    )

    doc = FSInputFile(file_path)
    await call.message.delete()

    await call.bot.send_document(
        chat_id=call.message.chat.id,
        document=doc,
        caption="⬆️ Нажмите, чтобы скачать и изучить методические материалы📄",
        reply_markup=keyboard
    )


@show_progress(total_steps=5, step_delay=0.05)
@catch_exceptions()
@check_file_exists('object_card_1')
async def object_card(call: CallbackQuery, file_path: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")]]
    )

    doc = FSInputFile(file_path)
    await call.message.delete()

    await call.bot.send_document(
        chat_id=call.message.chat.id,
        document=doc,
        caption="⬆️ Нажмите, чтобы скачать и изучить методические материалы📄",
        reply_markup=keyboard
    )


@show_progress(total_steps=5, step_delay=0.05)
@catch_exceptions()
@check_file_exists('vis_1')
async def add_vis_11(call: CallbackQuery, file_path: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")]]
    )

    doc = FSInputFile(file_path)
    await call.message.delete()

    await call.bot.send_document(
        chat_id=call.message.chat.id,
        document=doc,
        caption="⬆️ Нажмите, чтобы скачать и шаблон заявки для ввода📄",
        reply_markup=keyboard
    )


@show_progress(total_steps=5, step_delay=0.05)
@catch_exceptions()
@check_file_exists('vis_2')
async def add_vis_22(call: CallbackQuery, file_path: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")]]
    )

    doc = FSInputFile(file_path)
    await call.message.delete()

    await call.bot.send_document(
        chat_id=call.message.chat.id,
        document=doc,
        caption="⬆️ Нажмите, чтобы скачать и изучить методические материалы📄",
        reply_markup=keyboard
    )


@show_progress(total_steps=5, step_delay=0.05)
@catch_exceptions()
@check_file_exists('tim1')
async def add_tim_1(call: CallbackQuery, file_path: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")]]
    )

    doc = FSInputFile(file_path)
    await call.message.delete()

    await call.bot.send_document(
        chat_id=call.message.chat.id,
        document=doc,
        caption="⬆️ Нажмите, чтобы скачать и изучить методические материалы📄",
        reply_markup=keyboard
    )


@show_progress(total_steps=5, step_delay=0.05)
@catch_exceptions()
@check_file_exists('tim2')
async def add_tim_2(call: CallbackQuery, file_path: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")]]
    )

    doc = FSInputFile(file_path)
    await call.message.delete()

    await bot.send_document(
        chat_id=call.message.chat.id,
        document=doc,
        caption="⬆️ Нажмите, чтобы скачать и изучить методические материалы📄",
        reply_markup=keyboard
    )


@show_progress(total_steps=5, step_delay=0.05)
@catch_exceptions()
@check_file_exists('dock_1')
async def add_dock_1(call: CallbackQuery, file_path: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")]]
    )

    doc = FSInputFile(file_path)

    await call.message.delete()  # Удаление сообщения

    await bot.send_document(
        chat_id=call.message.chat.id,
        document=doc,
        caption="⬆️ Нажмите, чтобы скачать и изучить методические материалы📄",
        reply_markup=keyboard
    )

@show_progress(total_steps=5, step_delay=0.05)
@catch_exceptions()
@check_file_exists('road')
async def send_road(call: CallbackQuery, file_path: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")]]
    )

    doc = FSInputFile(file_path)

    await call.message.delete()  # Удаление сообщения

    await bot.send_document(
        chat_id=call.message.chat.id,
        document=doc,
        caption="⬆️ Нажмите, чтобы скачать и изучить методические материалы📄",
        reply_markup=keyboard
    )

@show_progress(total_steps=5, step_delay=0.05)
@catch_exceptions()
@check_file_exists('instruction_schedule')
async def send_keg_instruction(call: CallbackQuery, file_path: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")]]
    )

    doc = FSInputFile(file_path)

    await call.message.delete()  # Удаление сообщения

    await bot.send_document(
        chat_id=call.message.chat.id,
        document=doc,
        caption="⬆️ Нажмите, чтобы скачать и изучить методические материалы📄",
        reply_markup=keyboard
    )


# Асинхронная отправка файла (шаблон импорта объектов)
@show_progress(total_steps=5, step_delay=0.05)
async def send_add_object_file(call: CallbackQuery):
    file_path = file_attachments['add_object']
    doc = FSInputFile(file_path)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")]
        ]
    )
    try:
        await call.message.delete()  # Удаляем предыдущее сообщение
    except Exception as e:
        logging.warning(f"Не удалось удалить сообщение: {e}")
    await bot.send_document(
        chat_id=call.message.chat.id,
        document=doc,
        caption="Шаблон необходимо заполнить и отправить на email:📩 isup@kgexpert.ru",
        reply_markup=keyboard
    )


async def send_add_user_file(call: CallbackQuery):
    file_path = file_attachments['add_user']
    doc = FSInputFile(file_path)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")]
        ]
    )
    try:
        await call.message.delete()  # Удаляем предыдущее сообщение
    except Exception as e:
        logging.warning(f"Не удалось удалить сообщение: {e}")
    await bot.send_document(
        chat_id=call.message.chat.id,
        document=doc,
        caption=(
            "Шаблон необходимо заполнить и отправить на email:📩 isup@kgexpert.ru\n\n"
            "❗❗❗❗ **ВАЖНО!** ❗❗❗❗\n\n"
            "Обращаем Ваше внимание, что:\n"
            "• Электронная почта у каждого пользователя должна быть индивидуальной (не повторяться с другими пользователями)!\n"
            "• Электронная почта должна иметь домен '.ru'!"
        ),
        reply_markup=keyboard
    )

async def send_subscription_links(call: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Рабочий чат", url="https://t.me/+ObD-6zTF1ngzNjgy")],
            [InlineKeyboardButton(text="🔗 Официальный канал ИСУП", url="https://t.me/isup_KK")],
            [InlineKeyboardButton(text="🔗 Канал зам. руководителя деп. строительства Краснодарского края\nкурирующего ИСУП, Артема Моисеева",
    url="https://t.me/moiseevArtemA")],
            [InlineKeyboardButton(text="🔙 В главное меню", callback_data="menu:back")]
        ]
    )
    await call.message.edit_text(
        "📲 Подпишитесь на важные каналы для получения актуальной информации:",
        reply_markup=keyboard
    )

async def send_documents_link(call: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌐 Открыть 📂", url="https://cloud.mail.ru/public/UXKs/8rfz3hx5P")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")]
        ]
    )
    await call.message.edit_text(
        "📄 В облачном хранилище собраны все актуальные документы НПА..\n\n"
        "🔗 <b>Нажмите кнопку ниже, чтобы ознакомиться:</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

async def info1(call: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌐 Открыть 📂", url="https://cloud.mail.ru/public/qWYN/gkQvCBHbA")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")]
        ]
    )
    await call.message.edit_text(
        "📄 В облачном хранилище, собрана актуальная справочная информация.\n\n"
        "🔗 <b>Нажмите кнопку ниже, чтобы ознакомиться:</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@dp.callback_query(F.data == "submenu:forgot_password")
async def forgot_password_handler(call: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")]
        ]
    )
    await call.message.edit_text(text_answers["forgot_password"], reply_markup=keyboard)


async def block_user1(call: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")]
        ]
    )
    await call.message.edit_text(text_answers["block_text"], reply_markup=keyboard)


@dp.callback_query(F.data == "submenu:issue_digital_signature")
async def issue_digital_signature(call: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")]
        ]
    )
    await call.message.edit_text(
        text=text_answers["electronic_signature"],
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@dp.message(StateFilter(Feedback.waiting_for_message))
async def process_feedback_message(message: types.Message, state: FSMContext):
    user_message = message.text
    user_name = message.from_user.full_name
    user_id = message.from_user.id

    for admin_id in ADMIN_IDS:
        await bot.send_message(
            admin_id,
            f"📝 Новое сообщение от пользователя:\n\n"
            f"👤 Имя пользователя: {user_name} (ID: {user_id})\n\n"
            f"📩 Сообщение: {user_message}"
        )

    # Отправляем пользователю ответ и запоминаем ID сообщения
    confirmation_msg = await message.answer(
        f"✅ Спасибо {user_name} за обратную связь! Ваше сообщение отправлено администратору."
    )

    # Сохраняем ID сообщения в состояние
    await state.update_data(feedback_msg_id=confirmation_msg.message_id)

    await state.clear()

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
