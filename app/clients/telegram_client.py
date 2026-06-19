import requests

from app.config import Config

class TelegramClient:
    def __init__(self):
        self.bot_token = Config.TELEGRAM_BOT_TOKEN
        self.chat_id = Config.TELEGRAM_CHAT_ID
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def send_message(self, message: str) -> bool:
        if not self.bot_token or not self.chat_id:
            print("Telegram токен или Chat ID не настроены")
            return False

        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }

        try:
            response = requests.post(self.api_url, json=payload, timeout=30)
            response.raise_for_status()
            return True

        except requests.exceptions.RequestException as e:
            print(f"Ошибка отправки уведомления в Telegram: {e}")
            return False
