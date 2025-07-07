from middlewares.user_tracker import UserTrackerMiddleware
import asyncio
from utils import *
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, FSInputFile
)
from handlers import (
    add_tim_1,
    add_tim_2,
    add_contr,
    add_vis_11,
    add_vis_22,
    send_add_object_file,
    forgot_password_handler,
    send_keg_instruction,
    back_to_previous_menu,
    send_add_user_file,
    send_subscription_links,
    send_documents_link,
    issue_digital_signature,
    info1,
    send_road,
    add_dock_1,
    object_card,
    construction_control1,
    sign_participants1,
    upload_pd_rd1,
    exchange_docs1,
    block_user1,
    tech_support1
)
from utils import main_menu, return_to_main_menu, return_to_main_menu7
from aiogram.filters import CommandStart
sys.path.append(os.path.join(os.path.dirname(__file__), 'text1.py'))
from text1 import text_answers
import logging
from database import init_db, add_user
from dotenv import load_dotenv


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
dp.message.middleware(UserTrackerMiddleware())
dp.callback_query.middleware(UserTrackerMiddleware())

class Feedback(StatesGroup):
    waiting_for_message = State()

logging.basicConfig(level=logging.INFO)


@dp.message(CommandStart())
async def start_command(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Не указан"

    await add_user(user_id, username)  # Сохраняем пользователя в БД

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
                [InlineKeyboardButton(text="📑 Добавление контрактов на ПИР и СМР", callback_data="submenu:add_contr_1")],
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

        elif call.data == "submenu:add_contr_1":
            await add_contr(call)

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

        elif call.data == "submenu:tech_support":
            await tech_support1(call)


        await call.answer()

    except Exception as e:
        logging.error(f"Ошибка обработки callback: {e}")
        await call.answer("Кнопка не сработала ⚠️ Произошла ошибка,Пожалуйста перезапустите бота, очистите историю переписки с ботом и нажмите /start заново, чтобы всё заработало корректно.", show_alert=True)


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
    await init_db()  # Создаём БД перед запуском
    await dp.start_polling(bot)  # Запуск polling для бота
if __name__ == "__main__":
    asyncio.run(main())