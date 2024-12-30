from django.db import models

ENTITY_TYPE = (
    ("factory", "Завод"),
    ("retail", "Розничная сеть"),
    ("sole trader", "Индивидуальный предприниматель"),
)


class Entity(models.Model):
    entity_type = models.CharField(
        max_length=255, choices=ENTITY_TYPE, verbose_name="Тип огранизации"
    )
    name = models.CharField(max_length=255, verbose_name="Название организации")

    email = models.EmailField(unique=True, verbose_name="Email")
    country = models.CharField(max_length=255, verbose_name="Страна")
    city = models.CharField(max_length=255, verbose_name="Город")
    street = models.CharField(max_length=255, verbose_name="Улица")
    house_number = models.CharField(max_length=255, verbose_name="Номер дома")

    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients",
        verbose_name="Поставщик оборудования",
    )
    hierarchy_level = models.IntegerField(
        editable=False, verbose_name="Уровень иерархии", default=0
    )
    debt = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        verbose_name="Задолженность перед поставщиком",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время создания"
    )

    def save(self, *args, **kwargs):
        if self.entity_type == "factory":
            self.hierarchy_level = 0
        else:
            if self.supplier:
                self.hierarchy_level = self.supplier.hierarchy_level + 1

        if self.supplier == self:
            raise ValueError("Организация не может быть своим поставщиком.")

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"
        ordering = ["name", "hierarchy_level"]

    def __str__(self):
        return f"{self.name} ({self.entity_type}, {self.email})"


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название продукта")
    model = models.CharField(max_length=255, verbose_name="Модель продукта")
    release_date = models.DateField(verbose_name="Дата выхода на рынок")
    organization = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Организация",
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "release_date"]

    def __str__(self):
        return f"{self.name} ({self.model}, {self.release_date})"
