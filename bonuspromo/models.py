from django.db import models
from django.db.models import ForeignKey


# таблица с продукти на промоция. Не може да се повтаря един и същи продукт
class PromoConditionsPercent(models.Model):
    product_id = models.CharField(
        max_length = 9,
        unique = True,
        verbose_name = "ID на продукт"
    )
    product_name = models.CharField(
        max_length=20,
        verbose_name="Име на продукт"
    )
    purchasing_price = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name="Покупна цена за изчисление на отстъпката"
    )
    percent_discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Процент отстъпка за промоционалните продажби"
    )

    def __str__(self):
        return f"{self.product_id} | {self.product_name} | {self.percent_discount}%"

# Един продукт може да има няколко реда с продажби
class SalesQTY(models.Model):
    product_id = models.ForeignKey(
        PromoConditionsPercent,
        on_delete=models.CASCADE
    )
    sold_qty = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Количество продажби"
    )

    def __str__(self):
        return f"{self.product_id} ({self.sold_qty})"


