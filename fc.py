import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

BOT_TOKEN = "8979338262:AAH4ReFnRjIx07vwjrVYCKxMVf5EvjvgTnU"
CHANNEL_USERNAME = "FC_PROUZ"
WEBSITE_URL = "https://enasiba344-commits.github.io/Fcmobile2026/"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ==================== STIKERLAR (Xavfsiz yuborish funksiyasi bilan) ====================
STK_WELCOME = "CAACAgIAAxkBAAIBY2V_sample1"
STK_WARN = "CAACAgIAAxkBAAIBY2V_sample2"
STK_NEWS = "CAACAgIAAxkBAAIBY2V_sample3"
STK_FIRE = "CAACAgIAAxkBAAIBY2V_sample4"
STK_TACTIC = "CAACAgIAAxkBAAIBY2V_sample5"

async def send_safe_sticker(message: types.Message, sticker_id: str):
    """Stiker file_id xatosi bergan taqdirda bot to'xtab qolmasligini ta'minlaydi"""
    try:
        await message.answer_sticker(sticker_id)
    except Exception as e:
        logging.warning(f"Stiker yuborishda xatolik (file_id xato bo'lishi mumkin): {e}")

# ==================== INLINE MAJBURITY OBUNA & SAYT TUGMALARI ====================
def get_sub_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 FC PRO UZ kanaliga kirish", 
                    url=f"https://t.me/{CHANNEL_USERNAME}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌐 Bizning Rasmiy Saytga o'tish", 
                    url=WEBSITE_URL
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Obunani tasdiqlash", 
                    callback_data="check_subscription"
                )
            ]
        ]
    )

def get_site_inline_btn():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌐 FC Mobile 2026 Saytiga o'tish", 
                    url=WEBSITE_URL
                )
            ]
        ]
    )

# ==================== 14 TA TUGMALI ASOSIY MENYU ====================
def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🌐 Bizning Rasmiy Sayt"),
                KeyboardButton(text="⚡ So'nggi Yangiliklar")
            ],
            [
                KeyboardButton(text="🔥 Yangi Eventlar"),
                KeyboardButton(text="💎 Bozor & Narxlar")
            ],
            [
                KeyboardButton(text="🃏 TOP Kartalar"),
                KeyboardButton(text="🏆 Rank ko'tarish")
            ],
            [
                KeyboardButton(text="🎮 Taktika & Sxemalar"),
                KeyboardButton(text="🎯 Dribling va Fintlar")
            ],
            [
                KeyboardButton(text="🧤 Darvozabon Taktikasi"),
                KeyboardButton(text="⚔️ Turnirlar & Musobaqalar")
            ],
            [
                KeyboardButton(text="👥 Tarkibni baholash"),
                KeyboardButton(text="💬 Chatga kirish")
            ],
            [
                KeyboardButton(text="👨‍💻 Admin bilan aloqa"),
                KeyboardButton(text="🔄 Obunani tekshirish")
            ]
        ],
        resize_keyboard=True,
        persistent=True
    )

# ==================== OBUNANI TEKSHIRISH FUNKSIYASI ====================
async def check_user_sub(user_id: int) -> bool:
    try:
        chat_id = f"@{CHANNEL_USERNAME}" if not CHANNEL_USERNAME.startswith("-100") else CHANNEL_USERNAME
        member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        return member.status in ["creator", "administrator", "member"]
    except Exception as e:
        logging.error(f"Obuna tekshirishda xatolik (Bot kanalda admin ekanligiga ishonch hosil qiling): {e}")
        return False

async def require_subscription(message: types.Message) -> bool:
    user_id = message.from_user.id
    if not await check_user_sub(user_id):
        await send_safe_sticker(message, STK_WARN)
        await message.answer(
            f"🛑 **DIQQAT: Kirish taqiqlangan!**\n\n"
            f"Botning premium funksiyalaridan va eksklyuziv ma'lumotlardan foydalanish uchun "
            f"avval **@{CHANNEL_USERNAME}** rasmiy kanalimizga obuna bo'lishingiz shart!\n\n"
            f"👇 *Paski tugmalar orqali kanalga o'ting va obunani tasdiqlang:*",
            reply_markup=get_sub_keyboard(),
            parse_mode="Markdown"
        )
        return False
    return True 


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    if await check_user_sub(message.from_user.id):
        await send_safe_sticker(message, STK_WELCOME)
        await message.answer(
            f"Salom, **{message.from_user.full_name}**! 👋\n\n"
            f"⚽ **FC PRO UZ** interaktiv va eksklyuziv botiga xush kelibsiz!\n\n"
            f"Siz FC Mobile 2026 va EA FC olamidagi eng so'nggi yangiliklar, bozor tahlillari hamda "
            f"top taktikalar haqida ma'lumotlarni birinchi bo'lib olishingiz mumkin.\n\n"
            f"🌐 Bizning web-saytimiz: {WEBSITE_URL}\n\n"
            f"👇 **Paski 14 ta maxsus tugma orqali kerakli bo'limni tanlang:**",
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await send_safe_sticker(message, STK_WARN)
        await message.answer(
            f"Salom, **{message.from_user.full_name}**! ✋\n\n"
            f"Botdan to'liq foydalanish va barcha 14 ta menyuni ochish uchun "
            f"avval **@{CHANNEL_USERNAME}** kanalimizga a'zo bo'ling!",
            reply_markup=get_sub_keyboard(),
            parse_mode="Markdown"
        )

@dp.callback_query(F.data == "check_subscription")
async def check_sub_callback(callback: types.CallbackQuery):
    if await check_user_sub(callback.from_user.id):
        try:
            await callback.message.delete()
        except Exception:
            pass
        await send_safe_sticker(callback.message, STK_WELCOME)
        await callback.message.answer(
            "✅ **Muvaffaqiyatli tasdiqlandi!**\n\n"
            "Xush kelibsiz! Barcha 14 ta maxsus bo'lim va tugmalar aktivlashtirildi. "
            "Kerakli bo'limni tanlang:",
            reply_markup=get_main_keyboard()
        )
    else:
        await callback.answer("❌ Siz hali kanalimizga obuna bo'lmadingiz! Avval kanalga qo'shiling.", show_alert=True)

# ------------------- 14 TA TUGMA JAVOBLARI -------------------

@dp.message(F.text == "🌐 Bizning Rasmiy Sayt")
async def btn_website(message: types.Message):
    if not await require_subscription(message): return
    await message.answer(
        f"🌐 **FC Mobile 2026 Rasmiy Veb-sayti!**\n\n"
        f"Saytimiz orqali siz yangiliklarni to'liqroq o'qishingiz, maxsus gid va maqolalar bilan tanishishingiz mumkin.\n\n"
        f"🔗 Sayt manzili: {WEBSITE_URL}",
        reply_markup=get_site_inline_btn(),
        parse_mode="Markdown"
    )

@dp.message(F.text == "⚡ So'nggi Yangiliklar")
async def btn_1(message: types.Message):
    if not await require_subscription(message): return
    await send_safe_sticker(message, STK_NEWS)
    await message.answer(
        "📰 **EA FC & FC Mobile — So'nggi va Tezkor Yangiliklar:**\n\n"
        "1. **Mavsumiy Yangilanish:** O'yinga yangi afsonaviy kartalar to'plami va maxsus 'Team of the Week' kartalari qo'shildi.\n"
        "2. **O'yin Fizikasi:** Oxirgi patchda zarba berish aniqligi hamda darvozabonlarning reaksiya tezligi sezilarli darajada yaxshilandi.\n"
        "3. **Server Stabilizatsiyasi:** Ishlab chiquvchilar onlayn matchlardagi 'ping' muammolarini bartaraf etishdi.\n\n"
        "📌 *Barcha batafsil rasmiy e'lonlar saytimizda hamda **@FC_PROUZ** kanalida!*",
        reply_markup=get_site_inline_btn(),
        parse_mode="Markdown"
    )

@dp.message(F.text == "🔥 Yangi Eventlar")
async def btn_2(message: types.Message):
    if not await require_subscription(message): return
    await send_safe_sticker(message, STK_FIRE)
    await message.answer(
        "🔥 **Hozirda O'yinda Kechayotgan va Kutilayotgan Eventlar:**\n\n"
        "• **Klub Afsonalari Eventi:** Har kuni topshiriqlarni bajarib, tekin OVR 98+ kartalarni qo'lga kiriting.\n"
        "• **Muntazam Mashg'ulotlar:** Kunlik skill-game va uchrashuvlarni o'tkazib yubormang, ular sizga qimmatli moddiy resurslar beradi.\n"
        "• **Navbatdagi Event:** Kelayotgan juma kuni katta 'TOTS / TOTY' turidagi eksklyuziv voqelik kutilmoqda!",
        parse_mode="Markdown"
    )

@dp.message(F.text == "💎 Bozor & Narxlar")
async def btn_4(message: types.Message):
    if not await require_subscription(message): return
    await message.answer(
        "💎 **Bozor Tahlili va Investorlar uchun Maslahatlar:**\n\n"
        "📈 **Sotib olish vaqti:** Payshanba kuni (haftalik sovg'alar tarqatilganda narxlar 15-20% ga tushadi).\n"
        "📉 **Sotish vaqti:** Dam olish kunlari (Shanba va Yakshanba) talab ortgan paytda kartalaringizni qimmatroq soting.\n"
        "💡 **Investitsiya:** Hozirda 95+ OVR kartalarni zaxiraga olib qo'yish eng foydali strategiyadir.",
        parse_mode="Markdown"
    )

@dp.message(F.text == "🃏 TOP Kartalar")
async def btn_5(message: types.Message):
    if not await require_subscription(message): return
    await message.answer(
        "🃏 **O'yindagi Eng Kuchli (META) Kartalar Top-5:**\n\n"
        "1. **ST (Hujumchi):** Ronaldo Nazário / Erling Haaland — Yuqori tezlik va aniq zarba.\n"
        "2. **CAM (Pasyor):** Zinédine Zidane / Ruud Gullit — Maydonni mukammal ko'rish.\n"
        "3. **CB (Himoyachi):** Virgil van Dijk / Paolo Maldini — O'tib bo'lmas devor.\n"
        "4. **GK (Darvozabon):** Thibaut Courtois — Uzun bo'y va ajoyib retsidiv.\n\n"
        "📌 *To'liq statistika **@FC_PROUZ** kanalida va veb-saytimizda!*",
        reply_markup=get_site_inline_btn(),
        parse_mode="Markdown"
    )

@dp.message(F.text == "🏆 Rank ko'tarish")
async def btn_6(message: types.Message):
    if not await require_subscription(message): return
    await message.answer(
        "🏆 **O'yinchilar Rankini va Mashtabini Oshirish Qo'llanmasi:**\n\n"
        "• **Masherano / Dudek:** Rank oshiruvchi kartalardan unumli foydalaning. Rank 3 ga yetguncha 100% ehtimollik bilan oshiring.\n"
        "• **Training (Mashg'ulot):** O'yinchilarni kamida 15-20 darajagacha mashq qildiring. Bu ularning tezligi va kuchi uchun juda muhim.\n"
        "• **Skill Points:** Hujumchilar uchun 'Shooting/Pace', himoyachilar uchun 'Defending' nuqtalarini tanlang.",
        parse_mode="Markdown"
    )

@dp.message(F.text == "🎮 Taktika & Sxemalar")
async def btn_7(message: types.Message):
    if not await require_subscription(message): return
    await send_safe_sticker(message, STK_TACTIC)
    await message.answer(
        "🎮 **Hozirgi Navbatdagi Eng Kuchli (META) Sxemalar:**\n\n"
        "⚽ **4-3-3 Attack:** Tezkor qanot hujumlari va markaziy bosim uchun ideal.\n"
        "⚽ **4-1-2-1-2 Narrow:** Qisqa va aniq paslar bilan raqib mudofaasini yorib o'tish uchun maslahat beriladi.\n"
        "⚽ **5-2-1-2:** Himoyani jiddiy ushlab, qarshi hujumda raqibni tutish uchun eng ma'qul sxema.",
        parse_mode="Markdown"
    )

@dp.message(F.text == "🎯 Dribling va Fintlar")
async def btn_8(message: types.Message):
    if not await require_subscription(message): return
    await message.answer(
        "🎯 **Top 3 Eng Samarali Fintlar (Skill Moves):**\n\n"
        "1. **Lane Change:** Himoyachini osongina aldab o'tish va jarima maydonchasiga kirish uchun #1 fint.\n"
        "2. **Heel to Heel:** Tezlikni keskin oshirish va himoyachidan qochib ketish uchun ishlatiladi.\n"
        "3. **Open Up Fake Shot:** Darvozabon va himoyachilarni chalg'itib, qulay zarba pozitsiyasini yaratadi.",
        parse_mode="Markdown"
    )

@dp.message(F.text == "🧤 Darvozabon Taktikasi")
async def btn_9(message: types.Message):
    if not await require_subscription(message): return
    await message.answer(
        "🧤 **Darvozabonni Mukammal Boshqarish Sirlari:**\n\n"
        "• **GK Rush (Oldinga chiqarish):** Raqib hujumchisi yakkama-yakka chiqqanda '2nd Defend' tugmasini pastga torting.\n"
        "• **Burchak zarbalari:** Burchak zarbasi tepilayotganda darvozabonni ushlab, darvoza markaziga suring.\n"
        "• **Tanlov:** Bo'yi 195 sm dan baland va 'GK Long Throw' xususiyati bor darvozabonlarni tanlang.",
        parse_mode="Markdown"
    )

@dp.message(F.text == "⚔️ Turnirlar & Musobaqalar")
async def btn_10(message: types.Message):
    if not await require_subscription(message): return
    await message.answer(
        "⚔️ **FC PRO UZ Musobaqalari hamda Turnirlari:**\n\n"
        "🏆 Bizning kanalda va saytimizda muntazam ravishda pullik va bepul 1v1 kibersport turnirlari o'tkazib boriladi!\n\n"
        "📌 **Sovrinlar:** Real pul mukofotlari, Star Pass va qimmatbaho koinlar.\n"
        "Turnir qoidalari va ro'yxatdan o'tish uchun e'lonlarni kuzatib boring!",
        reply_markup=get_site_inline_btn(),
        parse_mode="Markdown"
    )

@dp.message(F.text == "👥 Tarkibni baholash")
async def btn_11(message: types.Message):
    if not await require_subscription(message): return
    await message.answer(
        "👥 **Tarkibni Professional Baholash va Maslahat:**\n\n"
        "Tarkibingiz skrinshotini oling va adminimizga yuboring. Adminimiz sizga:\n"
        "1. Qaysi pozitsiyani kuchaytirish kerakligini;\n"
        "2. Qaysi o'yinchini sotish to'g'ri bo'lishini;\n"
        "3. Qaysi taktikani qo'llash ma'qulligini tekinga aytib beradi!\n\n"
        "📩 **Murojaat uchun Admin:** @FC_PROUZ_ADMIN",
        parse_mode="Markdown"
    )

@dp.message(F.text == "💬 Chatga kirish")
async def btn_12(message: types.Message):
    if not await require_subscription(message): return
    await message.answer(
        "💬 **FC PRO UZ Muxlislar va Geymerlar Chati:**\n\n"
        "Chatda siz boshqa o'yinchilar bilan muloqot qilishingiz, do'stona matchlar o'tkazishingiz "
        "va o'z tarkibingizni muhokama qilishingiz mumkin!\n\n"
        "👉 **Chatga qo'shilish:** https://t.me/+IsIXNBO7k2Q1Y2Vi",
        parse_mode="Markdown"
    )

@dp.message(F.text == "👨‍💻 Admin bilan aloqa")
async def btn_13(message: types.Message):
    await message.answer(
        "👨‍💻 **Admin Bilan Bog'lanish:**\n\n"
        "• Savollar va takliflar uchun;\n"
        "• Reklama va hamkorlik masalalari bo'yicha;\n"
        "• Turnirga yozilish uchun;\n\n"
        "📩 **Admin:** @N_57001",
        parse_mode="Markdown"
    )

@dp.message(F.text == "🔄 Obunani tekshirish")
async def btn_14(message: types.Message):
    if await require_subscription(message):
        await message.answer("✅ **Ajoyib!** Siz kanalimiz a'zosisiz va barcha 14 ta tugma faol holatda!")

# ==================== MAIN ISHGA TUSHIRISH ====================
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())