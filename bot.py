import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message


TOKEN = os.getenv("TOKEN")

# ваш Telegram ID владельца
OWNER_ID = 5496034964


bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class OrderForm(StatesGroup):
    surname = State()
    name = State()
    patronymic = State()
    size = State()
    phone = State()
    address = State()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(
        "Здравствуйте! Для оформления заказа ответьте на вопросы.\n\n"
        "Введите вашу фамилию:"
    )
    await state.set_state(OrderForm.surname)


@dp.message(OrderForm.surname)
async def surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)

    await message.answer("Введите имя:")
    await state.set_state(OrderForm.name)


@dp.message(OrderForm.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer("Введите отчество:")
    await state.set_state(OrderForm.patronymic)


@dp.message(OrderForm.patronymic)
async def patronymic(message: Message, state: FSMContext):
    await state.update_data(patronymic=message.text)

    await message.answer("Введите размер одежды:")
    await state.set_state(OrderForm.size)


@dp.message(OrderForm.size)
async def size(message: Message, state: FSMContext):
    await state.update_data(size=message.text)

    await message.answer("Введите номер телефона:")
    await state.set_state(OrderForm.phone)


@dp.message(OrderForm.phone)
async def phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)

    await message.answer("Введите адрес доставки:")
    await state.set_state(OrderForm.address)


@dp.message(OrderForm.address)
async def address(message: Message, state: FSMContext):

    await state.update_data(address=message.text)

    data = await state.get_data()

    order = f"""
🛒 НОВЫЙ ЗАКАЗ

Фамилия: {data['surname']}
Имя: {data['name']}
Отчество: {data['patronymic']}

Размер одежды: {data['size']}

Телефон:
{data['phone']}

Адрес доставки:
{data['address']}
"""

    await bot.send_message(
        OWNER_ID,
        order
    )

    await message.answer(
        "Спасибо! Ваш заказ принят ✅"
    )

    await state.clear()


async def main():
    print("Бот запущен и ждёт заказов")
    await dp.start_polling(bot)


if name == "__main__":
    asyncio.run(main())
