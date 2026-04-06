import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import router
from database import init_db

async def main():
    # Создаём базу данных при первом запуске
    init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    print("✅ Бот запущен! Напиши ему в Telegram.")

    # Запускаем бота — он начинает получать сообщения
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())