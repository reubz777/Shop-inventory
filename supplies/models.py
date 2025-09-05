from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=256, verbose_name="Имя поставщика")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Поставщик"

