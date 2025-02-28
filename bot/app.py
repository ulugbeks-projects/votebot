import logging
from aiogram import executor
from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
)

async def on_startup(dispatcher):
    logging.info("Bot is starting...")

    # Birlamchi komandalar (/start va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)

    logging.info("Bot has started successfully.")


if __name__ == '__main__':
    logging.info("Starting bot...")
    executor.start_polling(dp, on_startup=on_startup)
