from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio


api = ""
bot = Bot(token= api)
dp = Dispatcher(bot, storage= MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

kb = InlineKeyboardMarkup()
button = InlineKeyboardButton(text= 'Рассчитать норму калорий', callback_data= 'calories')
button2 = InlineKeyboardButton(text= 'Формулы расчёта', callback_data='formulas')
kb.add(button)
kb.add(button2)
button_size = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text= 'Выберите опцию:') ],
        [
            KeyboardButton(text= 'Рассчитать норму калорий'),
            KeyboardButton(text= 'Формулы расчёта')
        ]
    ], resize_keyboard = True
)


@dp.message_handler(text= 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb)

@dp.callback_query_handler(text= 'formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес(кг) + 6,25 x рост(см)–5 х возраст(г) + 5')
    await call.answer()

@dp.callback_query_handler(text=['calories'])
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler(state= UserState.age)
async def set_growth(message, state):
    await state.update_data(first= message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state= UserState.growth)
async def set_weight(message, state):
    await state.update_data(second=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state= UserState.weight)
async def send_calories(message, state):
    await state.update_data(Thrird=message.text)
    data = await state.get_data()
    calories = 10 * float(data['Thrird']) + 6.25 * float(data['second']) - 5 * (float(data['first']) + 5)
    await message.answer(f'Ваша норма калорий: {calories}')
    await state.finish()

@dp.message_handler()
async def all_message(message):
    await message.answer("Пишите правильно!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)