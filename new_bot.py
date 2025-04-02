from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
import asyncio
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)

TOKEN = "7832695484:AAF48z_ifKvpO0Yc9oYiY1QBzQcvYnYiciA"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Храним данные о привычках пользователей
user_habits = {}

users_data = {}
# Главное меню

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔔 Напоминания", callback_data="menu:reminders")],
        [InlineKeyboardButton(text="📈 Контроль привычек", callback_data="menu:habits")],
        [InlineKeyboardButton(text="📅 Умный будильник", callback_data="menu:alarm")],
        [InlineKeyboardButton(text="💡 Советы", callback_data="menu:advice")],
    ])

@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer("👋 Привет! Я твой личный помощник.", reply_markup=main_menu())

# Контроль вредных привычек
@dp.callback_query(lambda c: c.data == "menu:habits")
async def habit_control(call: types.CallbackQuery):
    await call.message.answer("Введите привычку (например, 'бросить курить') и сумму экономии в день (например, 300):")
    user_habits[call.from_user.id] = {"start_date": datetime.now(), "habit": None, "saving": 0}

@dp.message()
async def habit_entry(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_habits and not user_habits[user_id]["habit"]:
        try:
            habit, saving = message.text.rsplit(" ", 1)
            saving = int(saving)
            user_habits[user_id]["habit"] = habit
            user_habits[user_id]["saving"] = saving
            await message.answer(f"Ты решил {habit}! Я буду следить за этим! 💪")
        except ValueError:
            await message.answer("Неверный формат. Введите привычку и сумму экономии, например: 'бросить курить 300'")

# Ежедневное уведомление о прогрессе
async def send_daily_update():
    while True:
        for user_id, data in user_habits.items():
            days = (datetime.now() - data["start_date"]).days
            total_saving = days * data["saving"]
            await bot.send_message(user_id, f"Ты сдерживаешься уже {days} дней! Экономия: {total_saving} руб.")
        await asyncio.sleep(86400)  # Ждем 24 часа

@dp.callback_query(lambda c: c.data == "smart_alarm")
async def set_alarm(call: types.CallbackQuery):
    await call.message.answer("Напиши время, когда тебя разбудить (формат HH:MM)")
    users_data[call.from_user.id] = {"state": "waiting_for_alarm"}

@dp.message()
async def handle_messages(message: types.Message):
    user_id = message.from_user.id
    if user_id in users_data and users_data[user_id].get("state") == "waiting_for_alarm":
        try:
            alarm_time = datetime.strptime(message.text, "%H:%M").time()
            users_data[user_id] = {"alarm_time": alarm_time}
            await message.answer(f"Будильник установлен на {message.text}")
            await check_alarm(user_id, alarm_time)
        except ValueError:
            await message.answer("Неверный формат времени. Попробуй еще раз.")

async def check_alarm(user_id, alarm_time):
    while True:
        now = datetime.now().time()
        if now.hour == alarm_time.hour and now.minute == alarm_time.minute:
            await bot.send_message(user_id, "⏰ Подъем! Время вставать!")
            break
        await asyncio.sleep(30)

# Напоминания о встречах
@dp.callback_query(lambda c: c.data == "meetings")
async def meetings(call: types.CallbackQuery):
    await call.message.answer("Напиши дату и время встречи (формат DD.MM HH:MM)")
    users_data[call.from_user.id] = {"state": "waiting_for_meeting"}

# Мотивация
@dp.callback_query(lambda c: c.data == "motivation")
async def motivation(call: types.CallbackQuery):
    await call.message.answer("Как твои успехи сегодня?")
    users_data[call.from_user.id] = {"state": "waiting_for_progress"}

@dp.message()
async def handle_progress(message: types.Message):
    user_id = message.from_user.id
    if user_id in users_data and users_data[user_id].get("state") == "waiting_for_progress":
        if "плохо" in message.text.lower():
            await message.answer("Не сдавайся! Завтра будет лучше! Вот анекдот для настроения: \n- Доктор, у меня бессонница. \n- Считайте овец. \n- Не помогает! \n- Тогда попробуйте считать долги. Заснете мгновенно!")
        else:
            await message.answer("Отлично! Держи темп!")

# Советы по психологии и питанию
@dp.callback_query(lambda c: c.data == "advice")
async def advice(call: types.CallbackQuery):
    advices = [
        "Пей больше воды и высыпайся!",
        "Не сравнивай себя с другими, твой путь уникален!",
        "Старайся есть больше овощей и фруктов!"
    ]
    await call.message.answer(advices[datetime.now().second % len(advices)])




if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(send_daily_update())
    loop.run_until_complete(dp.start_polling(bot))
