import requests
from datetime import datetime, timedelta

from app.config import Config


class WBClient:
    def __init__(self):
        self.token = Config.WB_TOKEN
        self.url = Config.WB_BASE_URL

    def get_yesterday_orders(self) -> list[dict]:
        # Формируем начало предыдущего дня в формате,
        # который ожидает Statistics API Wildberries
        yesterday = datetime.now() - timedelta(days=1)
        date_from_rfc = yesterday.strftime("%Y-%m-%dT00:00:00Z")

        headers = {
            "Authorization": self.token,
            "accept": "application/json",
        }

        params = {
            "dateFrom": date_from_rfc,
            "flag": 0,
        }

        try:
            response = requests.get(self.url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            # API возвращает список заказов
            # Дополнительная проверка оставлена на случай изменения формата ответа
            data = response.json()
            return data if isinstance(data, list) else data.get("orders", [])

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к WB API: {e}")
            return []