from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Tugmalarni yaratish
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛒 Buyurtma berish", callback_data="order")],
    [InlineKeyboardButton(text="💰 Balansni ko'rish", callback_data="balance")],
    [InlineKeyboardButton(text="🔗 Referal link", callback_data="referal")]
])