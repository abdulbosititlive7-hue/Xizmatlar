import asyncio
import os
import sqlite3
import requests
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# SOZLAMALAR
BOT_TOKEN = os.getenv("SMM_BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("SMM_BOT_TOKEN environment variable is not set")

API_URL = os.getenv("SMM_API_URL", "https://seensms.uz/api/v1")
API_KEY = os.getenv("SMM_API_KEY")
if not API_KEY:
    raise RuntimeError("SMM_API_KEY environment variable is not set")

SERVICE_PRICE_SUB = 1000 
STARS_PRICE = 5000000 

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# BAZA
conn = sqlite3.connect('referal.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                  (user_id INTEGER PRIMARY KEY, balance INTEGER, referrer_id INTEGER)''')
conn.commit()

# TUGMALAR
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍 Obunachi sotib olish"), KeyboardButton(text="⭐ Stars sotib olish")],
        [KeyboardButton(text="💳 Hisobim"), KeyboardButton(text="🎫 Referal")]
    ],
    resize_keyboard=True
)

class OrderState(StatesGroup):
    waiting_for_link = State()
    waiting_for_quantity = State()
    waiting_for_username = State()

# API FUNKSIYASI (Obunachi uchun)
def send_to_panel(link, quantity):
    # 'service': 1 qismini seensms.uz saytidagi kerakli xizmat ID raqamiga almashtiring
    data = {'key': API_KEY, 'action': 'add', 'service': 1, 'link': link, 'quantity': quantity}
    response = requests.post(API_URL, data=data)
    return response.json()

# HANDLERLAR
@dp.message(CommandStart())
async def start(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (user_id, 0, None))
        conn.commit()
    await message.answer("Xush kelibsiz! Tanlang:", reply_markup=main_menu)

@dp.message(F.text == "💳 Hisobim")
async def check_balance(message: types.Message):
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (message.from_user.id,))
    bal = cursor.fetchone()[0]
    await message.answer(f"Sizning balansingiz: {bal} ball.")

# OBUNACHI SOTIB OLISH
@dp.message(F.text == "🛍 Obunachi sotib olish")
async def start_order(message: types.Message, state: FSMContext):
    await message.answer("Kanal linkini yuboring:")
    await state.set_state(OrderState.waiting_for_link)

@dp.message(OrderState.waiting_for_link)
async def get_link(message: types.Message, state: FSMContext):
    await state.update_data(link=message.text)
    await message.answer("Nechta obunachi kerak?")
    await state.set_state(OrderState.waiting_for_quantity)

@dp.message(OrderState.waiting_for_quantity)
async def get_quantity(message: types.Message, state: FSMContext):
    try:
        qty = int(message.text)
        total_cost = qty * SERVICE_PRICE_SUB
        user_id = message.from_user.id
        
        cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        current_balance = cursor.fetchone()[0]
        
        if current_balance < total_cost:
            await message.answer(f"❌ Hisobingiz yetarli emas! Sizga {total_cost} ball kerak.")
        else:
            data = await state.get_data()
            result = send_to_panel(data['link'], qty)
            
            # API javobini tekshirish
            if "order" in result:
                cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (total_cost, user_id))
                conn.commit()
                await message.answer(f"✅ Buyurtma tasdiqlandi! ID: {result['order']}")
            else:
                await message.answer("❌ API xatoligi: buyurtma yuborilmadi.")
        await state.clear()
    except:
        await message.answer("❌ Xatolik! Iltimos, son kiriting.")

@dp.message(F.text == "⭐ Stars sotib olish")
async def buy_stars(message: types.Message, state: FSMContext):
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (message.from_user.id,))
    if cursor.fetchone()[0] < STARS_PRICE:
        await message.answer(f"❌ Hisobingiz yetarli emas!")
    else:
        await message.answer("Username-ni yozing:")
        await state.set_state(OrderState.waiting_for_username)

@dp.message(OrderState.waiting_for_username)
async def process_username(message: types.Message, state: FSMContext):
    cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (STARS_PRICE, message.from_user.id))
    conn.commit()
    await message.answer(f"✅ {message.text} uchun buyurtma qabul qilindi!")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())