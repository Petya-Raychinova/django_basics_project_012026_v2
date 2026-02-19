from django.db import models

# таблица с доставчици; Един доставчик може да има само едно условие
class ConditionsPercent(models.Model):
    on_delete = models.CASCADE
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

# Един доставчик може да има няколко реда с покупки
class PurchasingAmount(models.Model):
    condition_eik = models.ForeignKey(
        ConditionsPercent,
        on_delete=models.CASCADE,
        related_name="ttlpurchases",
        null=False,
        blank=False
    )
    purchasing_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.condition_eik.eik} - {self.purchasing_amount}"





