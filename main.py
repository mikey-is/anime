import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TOKEN = "8646353568:AAH31cTO-LPeXOQtJyvNrLjw2RqxyjfVCYI"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# SIZNING TELEGRAM ID-INGIZ (Asosiy yaratuvchi sifatida shu yerga yozing)
# Masalan: 12345678 (O'zingizni ID-ingizni qo'ying, hozircha namunaviy)
SUPER_ADMIN = 7796591595

# Adminlar ro'yxati (Boshlanishiga siz va super admin)
ADMINS = [SUPER_ADMIN]

# --- 1. ADMIN BOSHQARUVI (YANGI ADMIN QO'ShISh) ---
@dp.message(Command("addadmin"))
async def add_admin_cmd(message: types.Message):
    if message.from_user.id != SUPER_ADMIN:
        return await message.answer("❌ Bu buyruq faqat asosiy admin uchun!")
    
    try:
        # Buyruq formati: /addadmin 12345678
        new_admin_id = int(message.text.split()[1])
        if new_admin_id not in ADMINS:
            ADMINS.append(new_admin_id)
            await message.answer(f"✅ Yangi admin muvaffaqiyatli qo'shildi! (ID: {new_admin_id})")
        else:
            await message.answer("ℹ️ Bu foydalanuvchi allaqachon admin.")
    except (IndexError, ValueError):
        await message.answer("⚠️ To'g'ri formatda yozing. Masalan: <code>/addadmin 12345678</code>", parse_mode="HTML")

# --- 2. ADMIN UCHUN: ANIME QO'ShISh (FILE ID OLISh) ---
@dp.message(lambda message: message.video)
async def get_video_id(message: types.Message):
    if message.from_user.id not in ADMINS:
        return # Oddiy foydalanuvchilarga javob bermaydi
        
    video_id = message.video.file_id
    await message.answer(
        f"🎬 <b>Yangi anime videosi ID-si aniqlandi:</b>\n\n<code>{video_id}</code>\n\n"
        f"<i>Buni nusxalab, kanaldagi post ostidagi tugmaga 'download_{video_id}' qilib joylaysiz.</i>", 
        parse_mode="HTML"
    )

# --- 3. FOYDALANUVChI TUGMANI BOSGANDA VEDIONI YUKLAB BERISh ---
@dp.callback_query(lambda call: call.data.startswith("download_"))
async def send_anime_video(call: types.CallbackQuery):
    video_id = call.data.split("_")[1]
    await call.answer("Anime yuklanmoqda, iltimos kuting...") 
    try:
        await bot.send_video(chat_id=call.from_user.id, video=video_id, caption="✨ Marhamat, siz so'ragan anime!")
    except Exception:
        await bot.send_message(chat_id=call.from_user.id, text="❌ Xatolik! Botni bloklamaganingizga ishonch hosil qiling.")

# --- 4. /start BUYRUG'I (SAYT TUGMASI BILAN) ---
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    # Bu yerga pastda o'zimiz yaratadigan chiroyli sakura saytining linkini qo'yamiz
    SAYT_LINKI = "https://mikey-is.github.io/anime/"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌸 Onlayn Saytni Ochish", web_app=WebAppInfo(url=SAYT_LINKI))]
    ])

    await message.answer(
        f"Salom {message.from_user.full_name}!\n"
        f"Anime botimizga xush kelibsiz. Sayt orqali onlayn ko'rish uchun pastdagi tugmani bosing: 👇",
        reply_markup=keyboard
    )

async def main():
    print("🚀 Bot (Admin panel va Sayt tizimi bilan) ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())