from django.core.exceptions import ValidationError
from django.db import models
from products.models import Batch
from django.utils import timezone

class Sale(models.Model):

    batch = models.ForeignKey(
        Batch,
        on_delete=models.PROTECT, # Защищаем от удаления партии, по которой были продажи
        related_name='sales',
        verbose_name="Партия товара"
    )
    quantity = models.PositiveIntegerField(default=1)
    sale_date = models.DateTimeField()

    class Meta:
        db_table = "Продажи"
        verbose_name = "Продажа"

    def formatted_date(self):
        return self.sale_date.strftime("%d.%m.%Y %H:%M")

    def clean(self):
        if self.quantity > self.batch.quantity:
            raise ValidationError(
                f"Недостаточно товара. В наличии: {self.batch.quantity}"
            )

    def save(self, *args, **kwargs):
        self.full_clean()

        if self._state.adding:
            self.batch.quantity -= self.quantity
            self.batch.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.batch)

