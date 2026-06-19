from collections import Counter
from datetime import datetime

from app.clients.wb_client import WBClient
from app.storage.csv_storage import CSVStorage
from app.clients.telegram_client import TelegramClient


class ReportService:
    def __init__(self):
        self.wb_client = WBClient()
        self.storage = CSVStorage()
        self.tg_client = TelegramClient()

    def run_daily_pipeline(self):
        orders = self.wb_client.get_yesterday_orders()
        if not orders:
            print("Заказы за вчерашний день не найдены или произошла ошибка API")
            return

        self.storage.save_orders(orders)

        # Исключаем отмененные заказы из расчета статистики
        articles = [order.get("supplierArticle") for order in orders if (order.get("supplierArticle")
                                                                         and not order.get("isCancel", False)
                                                                         )
                    ]
        top_3 = Counter(articles).most_common(3)

        lines = [
            "Ежедневный отчет по заказам",
            f"Дата генерации: {datetime.now().strftime('%d.%m.%Y')}",
            "",
            "Топ-3 артикула:",
        ]

        medals = ["🥇", "🥈", "🥉"]
        for i, (article, count) in enumerate(top_3):
            lines.append(f"{medals[i] if i < len(medals) else i} Артикул: `{article}` — *{count}* шт.")

        text = "\n".join(lines)
        self.tg_client.send_message(text)
