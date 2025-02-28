import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.data import config

# Initialize bot and dispatcher
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,  # You can change to DEBUG for more details
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler("bot.log", encoding='utf-8')  # Log to file
    ]
)

# Example usage (optional, can be removed if not needed)
logging.info("Bot is starting...")

# Optional: You can also add aiogram's own logger if needed
logging.getLogger('aiogram').setLevel(logging.INFO)
