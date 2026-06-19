import os
import csv

from datetime import datetime

from app.config import Config


class CSVStorage:
    def __init__(self):
        self.file_path = Config.CSV_OUTPUT_PATH

    def save_orders(self, orders: list[dict]) -> str:
        # Создаем директорию для CSV, если она отсутствует
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        fields_name = ["order_date", "article", "product_name", "status", "price"]

        with open(self.file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields_name)
            writer.writeheader()

            for order in orders:
                raw_date = order.get("date") or order.get("orderDate")
                try:
                    clean_date = datetime.fromisoformat(raw_date.replace("Z", "")).strftime("%d-%m-%Y")
                except (ValueError, TypeError):
                    clean_date = datetime.now().strftime("%d-%m-%Y")

                # Используем цену со скидкой, если она присутствует
                raw_price = order.get("priceWithDisc") or order.get("totalPrice", 0)
                try:
                    formatted_price = f"{float(raw_price):.2f}".replace(".", ",")
                except (ValueError, TypeError):
                    formatted_price = "0,00"

                writer.writerow({
                    "order_date": clean_date,
                    "article": order.get("supplierArticle") or order.get("nmId"),
                    "product_name": order.get("subject", "Неизвестный товар"),
                    "status": order.get("orderStatus") or "Новый",
                    "price": formatted_price
                })
        return self.file_path

