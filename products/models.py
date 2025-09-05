from django.db import models
from django.core.validators import MinValueValidator
from supplies.models import Supplier

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True,verbose_name="Имя категории")

    class Meta:
        db_table = "Категории"
        verbose_name = "Категория"
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name="Имя продукта")
    category = models.ForeignKey(
        Category,
        on_delete= models.SET_NULL,
        null=True,
        blank=True,
        related_name="category",
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete= models.SET_NULL,
        null=True,
        blank=True,
        related_name="supplier",
    )

    class Meta:
        db_table = "Товары"
        verbose_name = "Товар"


    def __str__(self):
        return self.name

    @property
    def total_quantity(self):
        return self.batches.aggregate(total=models.Sum('quantity'))['total'] or 0



class Batch(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='batches',
        verbose_name='Товар',
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Цена реализации"
    )

    quantity = models.IntegerField(
        default=0,
        blank=True,
        validators=[MinValueValidator(0)],
    )

    arrival_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата поступления партии"
    )

    class Meta:
        verbose_name = "Партия товара"
        ordering = ['arrival_date']

    def __str__(self):
        return f"Партия #{self.id} - {self.product.name} ({self.arrival_date.date()})"
