import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message


TOKEN = os.getenv("TOKEN")

# Telegram ID владельца
OWNER_ID = 431939187


bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class OrderForm(StatesGroup):
    surname = State()
    name = State()
    patronymic = State()
    size = State()
    phone = State()
    address = State()


# Старт
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):

    await state.clear()

    await message.answer(
        "Ассаляму алейкум уа рахматуЛлахи уа баракятуху!🌸 👋\n\n"
        "Для оформления заказа ответьте на несколько вопросов.\n\n"
        "Введите вашу фамилию:"
    )

    await state.set_state(OrderForm.surname)


# Фамилия
@dp.message(OrderForm.surname)
async def surname(message: Message, state: FSMContext):

    await state.update_data(
        surname=message.text
    )

    await message.answer(
        "Введите имя:"
    )

    await state.set_state(OrderForm.name)



# Имя
@dp.message(OrderForm.name)
async def name(message: Message, state: FSMContext):

    await state.update_data(
        name=message.text
    )

    await message.answer(
        "Введите отчество:"
    )

    await state.set_state(OrderForm.patronymic)



# Отчество
@dp.message(OrderForm.patronymic)
async def patronymic(message: Message, state: FSMContext):

    await state.update_data(
        patronymic=message.text
    )

    await message.answer(
        "Введите рост в см:"
    )

    await state.set_state(OrderForm.size)



# Размер
@dp.message(OrderForm.size)
async def size(message: Message, state: FSMContext):

    await state.update_data(
        size=message.text
    )

    await message.answer(
        "Введите номер телефона для связи:"
    )

    await state.set_state(OrderForm.phone)



# Телефон
@dp.message(OrderForm.phone)
async def phone(message: Message, state: FSMContext):

    await state.update_data(
        phone=message.text
    )

    await message.answer(
        "Доставка осуществляется через пункты выдачи вайлдберрис и озон🌸 Пожалуйста напишите адрес вашего пункта выдачи и привязанный номер телефона🌸  БаракаЛлаху фикум! :"
    )

    await state.set_state(OrderForm.address)



# Адрес и отправка заказа
@dp.message(OrderForm.address)
async def address(message: Message, state: FSMContext):

    await state.update_data(
        address=message.text
    )


    data = await state.get_data()


    # ссылка на клиента
    if message.from_user.username:

        client_link = (
            f"https://t.me/{message.from_user.username}"
        )

    else:

        client_link = (
            f"tg://user?id={message.from_user.id}"
        )


    order = f"""
🛒 НОВЫЙ ЗАКАЗ

👤 Чат с клиентом:
{client_link}


📌 Данные клиента:

Фамилия:
{data['surname']}

Имя:
{data['name']}

Отчество:
{data['patronymic']}


👕 Размер одежды:
{data['size']}


📞 Телефон:
{data['phone']}


📦 Адрес доставки:
{data['address']}
"""


    await bot.send_message(
        OWNER_ID,
        order
    )


    await message.answer(
        "Джазаки Аллаху хайран!🌸 Ваш заказ принят ✅\n\n"
        "Мы скоро свяжемся с вами."
    )


    await state.clear()



async def main():

    print("Бот запущен и принимает заказы")

    await dp.start_polling(bot)



if name == "__main__":

    asyncio.run(main())
