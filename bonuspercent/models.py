from django.db import models

# таблица с доставчици
class ConditionsPercent(models.Model):
    eik = models.CharField(
        max_length = 13,
        unique = True,
        verbose_name = "ЕИК на доставчик"
    )
    supplier_name = models.CharField(
        max_length=100,
        verbose_name="Име на доставчик"
    )
    percent_condition = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Процент бонус"
    )

    def __str__(self):
        return f"{self.supplier_name} ({self.percent_condition})"

class PurchasingAmount(models.Model):
    eik = models.CharField(
        max_length = 13,
        unique = True,
        verbose_name = "ЕИК на доставчик"
    )
    purchasing_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Стойност покупка"
    )

    def __str__(self):
        return f"{self.eik} ({self.purchasing_amount})"