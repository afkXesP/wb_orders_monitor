import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    # Wildberries API
    WB_TOKEN = os.getenv('WB_TOKEN', "").strip()
    WB_BASE_URL = "https://statistics-api.wildberries.ru/api/v1/supplier/orders"

    # Telegram API
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', "").strip()
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', "").strip()

    # Пути к файлам
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CSV_OUTPUT_PATH = os.path.join(BASE_DIR, 'data', 'orders.csv')
