import os
import sys
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types
from decorators_for_bot import show_progress, catch_exceptions, check_file_exists,file_attachments
from aiogram.types import FSInputFile
sys.path.append(os.path.join(os.path.dirname(__file__), 'text1.py'))
from text1 import text_answers
from utils import *

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

ADMIN_IDS = [1316342598]

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()

class Feedback(StatesGroup):
    waiting_for_message = State()


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


@show_progress(total_steps=5, step_delay=0.05)
@catch_exceptions()
@check_file_exists('add_contr_file')
async def add_contr(call: CallbackQuery, file_path: str):
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

@dp.callback_query(F.data == "submenu:tech_support")
async def tech_support1(call: CallbackQuery):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")]
        ]
    )
    await call.message.edit_text(
        text=text_answers["tech_support"],
        reply_markup=keyboard,
        parse_mode="HTML"
    )

