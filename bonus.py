import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)
from telegram.request import HTTPXRequest

# Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# --- KONFIGURATSIYA ---
BOT_TOKEN = "8947484775:AAElxrV4lc52bkUuhxJqEXKMsjpLKrMf_MQ"
ADMIN_ID = 8327302562

# Bosqichlar
SERVICE, LINK, QUANTITY = range(3)

# Ma'lumotlar bazasi
USERS = {}
ORDER_COUNTER = 1000

CATEGORIES = {
    "cat_tg": "📱 Telegram Xizmatlari",
    "cat_inst": "📸 Instagram Xizmatlari",
    "cat_yt": "▶️ YouTube Xizmatlari",
    "cat_tt": "🎵 TikTok Xizmatlari",
    "cat_pkg": "🎁 VIP SMM Paketlar",
}

SERVICES = {
    "tg_1": {"cat": "cat_tg", "name": "Telegram A'zo (Kafolatlangan)", "price": 12000},
    "tg_2": {"cat": "cat_tg", "name": "Telegram Ko'rishlar (Oxirgi 5 post)", "price": 2000},
    "tg_3": {"cat": "cat_tg", "name": "Telegram Avto-layk / Reaksiya", "price": 4000},
    "inst_1": {"cat": "cat_inst", "name": "Instagram Obunachi (Sifatli)", "price": 15000},
    "inst_2": {"cat": "cat_inst", "name": "Instagram Layk (Tezkor)", "price": 5000},
    "inst_3": {"cat": "cat_inst", "name": "Instagram Reels Ko'rishlar", "price": 3000},
    "yt_1": {"cat": "cat_yt", "name": "YouTube Ko'rishlar (HD)", "price": 25000},
    "yt_2": {"cat": "cat_yt", "name": "YouTube Obunachilar", "price": 45000},
    "tt_1": {"cat": "cat_tt", "name": "TikTok Obunachilar", "price": 18000},
    "tt_2": {"cat": "cat_tt", "name": "TikTok Ko'rishlar", "price": 2000},
    "pkg_1": {"cat": "cat_pkg", "name": "📦 Start Paket (1k Telegram + 1k Inst)", "price": 22000},
    "pkg_2": {"cat": "cat_pkg", "name": "🚀 PRO Paket (5k Inst Obunachi + 5k Layk)", "price": 85000},
}

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        [KeyboardButton("🛒 Xizmatlar Bo'limi")],
        [KeyboardButton("👤 Kabinet / Balans"), KeyboardButton("🔗 Referal Tizimi")],
    ],
    resize_keyboard=True
)


def get_user_data(user_id: int):
    if user_id not in USERS:
        USERS[user_id] = {"balance": 0, "referrals": 0, "referred_by": None}
    return USERS[user_id]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = get_user_data(user.id)

    if context.args and user_data["referred_by"] is None:
        try:
            referrer_id = int(context.args[0])
            if referrer_id != user.id and referrer_id in USERS:
                user_data["referred_by"] = referrer_id
                USERS[referrer_id]["balance"] += 50
                USERS[referrer_id]["referrals"] += 1

                try:
                    await context.bot.send_message(
                        chat_id=referrer_id,
                        text="SIZDA YANGI TAKLIF MAVJUD VA SIZNING HISOBINGIZGA 50 SO'M QO'SHILDI!"
                    )
                except Exception:
                    pass
        except ValueError:
            pass

    text = f"👋 **Xush kelibsiz, {user.first_name}!**\n\nQuyidagi tugmalar orqali kerakli bo'limni tanlang:"
    if update.message:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=MAIN_KEYBOARD)
    elif update.callback_query:
        await update.callback_query.message.reply_text(text, parse_mode="Markdown", reply_markup=MAIN_KEYBOARD)
    return ConversationHandler.END


async def show_cabinet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_data = get_user_data(user.id)

    text = (
        f"👤 **SHAXSIY KABINET**\n\n"
        f"🆔 **ID:** `{user.id}`\n"
        f"👤 **Ism:** {user.full_name}\n"
        f"💰 **Balansingiz:** `{user_data['balance']:,.0f} so'm`\n"
        f"👥 **Taklif qilgan do'stlaringiz:** `{user_data['referrals']} ta`"
    )
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=MAIN_KEYBOARD)


async def show_referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_data = get_user_data(user.id)
    bot_username = (await context.bot.get_me()).username

    ref_link = f"https://t.me/{bot_username}?start={user.id}"

    text = (
        f"🔗 **REFERAL DASTURI**\n\n"
        f"Do'stlaringizni taklif qiling va pul ishlang!\n"
        f"💵 **Har bir taklif uchun:** `50 so'm` beriladi.\n\n"
        f"📊 **Sizning ko'rsatkichlaringiz:**\n"
        f"• Taklif qilinganlar: `{user_data['referrals']} ta`\n"
        f"• Ishlangan pul: `{user_data['referrals'] * 50} so'm`\n\n"
        f"👇 **Sizning referal havolangiz:**\n`{ref_link}`"
    )
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=MAIN_KEYBOARD)


async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for cat_id, cat_name in CATEGORIES.items():
        keyboard.append([InlineKeyboardButton(cat_name, callback_data=cat_id)])

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text("📂 **Ijtimoiy tarmoqni tanlang:**", parse_mode="Markdown", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.edit_text("📂 **Ijtimoiy tarmoqni tanlang:**", parse_mode="Markdown", reply_markup=reply_markup)


async def show_services_by_cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    selected_cat = query.data
    keyboard = []

    for srv_id, srv_info in SERVICES.items():
        if srv_info["cat"] == selected_cat:
            keyboard.append([
                InlineKeyboardButton(
                    f"{srv_info['name']} - {srv_info['price']} so'm", 
                    callback_data=f"srv_{srv_id}"
                )
            ])

    keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_cats")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text("👇 **Kerakli xizmatni tanlang:**", parse_mode="Markdown", reply_markup=reply_markup)
    return SERVICE


async def select_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    service_id = query.data.replace("srv_", "")
    context.user_data["selected_service"] = service_id
    service = SERVICES[service_id]

    await query.message.edit_text(
        f"📌 Siz tanladingiz: **{service['name']}**\n"
        f"💵 Narxi: `{service['price']} so'm` (1000 ta uchun)\n\n"
        "🔗 **Buyurtma uchun havola (link) kiriting:**\n"
        "*(Masalan: https://t.me/kanal_nomi yoki https://instagram.com/username)*",
        parse_mode="Markdown",
    )
    return LINK


async def get_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text.strip()
    if not link.startswith("http://") and not link.startswith("https://") and not link.startswith("@"):
        await update.message.reply_text("❌ Noto'g'ri havola. Iltimos, to'liq link kiriting:")
        return LINK

    context.user_data["link"] = link
    await update.message.reply_text("🔢 Qancha miqdorda buyurtma qilmoqchisiz? (Masalan: 1000):")
    return QUANTITY


async def process_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ORDER_COUNTER
    user = update.message.from_user
    user_data = get_user_data(user.id)

    try:
        quantity = int(update.message.text.strip())
        if quantity < 10:
            await update.message.reply_text("❌ Eng kam buyurtma miqdori: 10 ta. Qaytadan kiriting:")
            return QUANTITY
    except ValueError:
        await update.message.reply_text("❌ Iltimos, faqat raqam kiriting:")
        return QUANTITY

    service_id = context.user_data.get("selected_service")
    if not service_id or service_id not in SERVICES:
        await update.message.reply_text("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.", reply_markup=MAIN_KEYBOARD)
        return ConversationHandler.END

    service = SERVICES[service_id]
    link = context.user_data["link"]
    total_price = (quantity / 1000) * service["price"]

    # --- BALANS TEKSHIRUVI VA PUL YECHISH ---
    if user_data["balance"] < total_price:
        await update.message.reply_text(
            f"❌ **Mablag' yetarli emas!**\n\n"
            f"💳 Buyurtma summasi: `{total_price:,.0f} so'm`\n"
            f"💰 Balansingiz: `{user_data['balance']:,.0f} so'm`\n\n"
            "Iltimos, balansingizni to'ldiring yoki kamroq miqdor kiriting.",
            parse_mode="Markdown",
            reply_markup=MAIN_KEYBOARD
        )
        return ConversationHandler.END

    # Balansdan pulni yechish
    user_data["balance"] -= total_price

    ORDER_COUNTER += 1
    order_id = ORDER_COUNTER

    text_user = (
        "🎉 **BUYURTMANGIZ QABUL QILINDI!** 🚀\n\n"
        f"🆔 **Buyurtma ID:** `{order_id}`\n"
        f"📌 **Xizmat:** {service['name']}\n"
        f"🔗 **Link:** {link}\n"
        f"📊 **Miqdor:** {quantity} ta\n"
        f"💰 **Jami summa:** {total_price:,.0f} so'm\n"
        f"💳 **Qolgan balans:** {user_data['balance']:,.0f} so'm\n\n"
        "⚡️ Buyurtmangiz tez orada bajariladi!"
    )

    text_admin = (
        "📥 **YANGI BUYURTMA KELDI!** 💥\n\n"
        f"🆔 **Buyurtma ID:** `{order_id}`\n"
        f"👤 **Mijoz:** {user.full_name} (@{user.username if user.username else 'yoq'})\n"
        f"🆔 **Mijoz ID:** `{user.id}`\n"
        f"📌 **Xizmat:** {service['name']}\n"
        f"🔗 **Link:** {link}\n"
        f"📊 **Miqdor:** {quantity} ta\n"
        f"💰 **Summa:** {total_price:,.0f} so'm"
    )

    admin_keyboard = [[
        InlineKeyboardButton("✅ BUYURTMANI BAJARILDI QILISH", callback_data=f"done_{order_id}_{user.id}")
    ]]

    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=text_admin,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(admin_keyboard)
        )
    except Exception as admin_err:
        logging.error(f"Adminga yuborishda xato: {admin_err}")

    await update.message.reply_text(text_user, parse_mode="Markdown", reply_markup=MAIN_KEYBOARD)
    return ConversationHandler.END


async def mark_order_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data_parts = query.data.split("_")
    order_id = data_parts[1]
    user_id = int(data_parts[2])

    try:
        user_msg = f"✨ **{order_id} BUYURTMANGIZ BAJARILDI!** 🎯✅\n\nXizmatimizdan foydalanganingiz uchun rahmat! 🚀"
        await context.bot.send_message(chat_id=user_id, text=user_msg, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Xabar yuborishda xato: {e}")

    await query.message.edit_text(
        f"{query.message.text}\n\n✅ **Ushbu buyurtma bajarildi deb belgilandi!**",
        parse_mode="Markdown"
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)
    return ConversationHandler.END


def main():
    request = HTTPXRequest(connect_timeout=60.0, read_timeout=60.0)
    app = Application.builder().token(BOT_TOKEN).request(request).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(show_services_by_cat, pattern="^cat_"),
            MessageHandler(filters.Regex("^🛒 Xizmatlar Bo'limi$"), show_categories)
        ],
        states={
            SERVICE: [
                CallbackQueryHandler(select_service, pattern="^srv_"),
                CallbackQueryHandler(show_categories, pattern="^back_to_cats$")
            ],
            LINK: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex("^(🛒 Xizmatlar Bo'limi|👤 Kabinet / Balans|🔗 Referal Tizimi)$"), get_link)
            ],
            QUANTITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex("^(🛒 Xizmatlar Bo'limi|👤 Kabinet / Balans|🔗 Referal Tizimi)$"), process_order)
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("start", start),
            MessageHandler(filters.Regex("^🛒 Xizmatlar Bo'limi$"), show_categories),
            MessageHandler(filters.Regex("^👤 Kabinet / Balans$"), show_cabinet),
            MessageHandler(filters.Regex("^🔗 Referal Tizimi$"), show_referral),
            CallbackQueryHandler(show_categories, pattern="^back_to_cats$"),
        ],
        allow_reentry=True
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    app.add_handler(MessageHandler(filters.Regex("^👤 Kabinet / Balans$"), show_cabinet))
    app.add_handler(MessageHandler(filters.Regex("^🔗 Referal Tizimi$"), show_referral))

    app.add_handler(CallbackQueryHandler(mark_order_done, pattern="^done_"))

    app.run_polling()


if __name__ == "__main__":
    main()index.htmlindex