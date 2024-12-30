from django.test import TestCase
from datetime import date
from .models import Entity, Product


class EntityModelTest(TestCase):
    def setUp(self):
        self.factory = Entity.objects.create(
            entity_type="factory",
            name="Завод 1",
            email="factory1@example.com",
            country="Россия",
            city="Москва",
            street="Ленина",
            house_number="1",
        )

        self.retail = Entity.objects.create(
            entity_type="retail",
            name="Розничная сеть 1",
            email="retail1@example.com",
            country="Россия",
            city="Санкт-Петербург",
            street="Пушкина",
            house_number="2",
            supplier=self.factory,
        )

    def test_entity_creation(self):
        """Проверяем правильность присвоения уровней иерархии"""
        self.assertEqual(self.factory.hierarchy_level, 0)
        self.assertEqual(self.retail.hierarchy_level, 1)

    def test_self_supplier_restriction(self):
        """Проверяем что нельзя указать себя в качестве поставщика"""
        with self.assertRaises(ValueError):
            entity = Entity(
                entity_type="sole trader",
                name="ИП 1",
                email="soletrader1@example.com",
                country="Россия",
                city="Казань",
                street="Советская",
                house_number="3",
                supplier=None,
            )
            entity.supplier = entity
            entity.save()

    def test_str_representation(self):
        """Проверяем метод представления str"""
        self.assertEqual(str(self.factory), "Завод 1 (factory, factory1@example.com)")
        self.assertEqual(str(self.retail), "Розничная сеть 1 (retail, retail1@example.com)")


class ProductModelTest(TestCase):
    def setUp(self):
        self.entity = Entity.objects.create(
            entity_type="factory",
            name="Завод 1",
            email="factory1@example.com",
            country="Россия",
            city="Москва",
            street="Ленина",
            house_number="1",
        )

        self.product = Product.objects.create(
            name="Продукт 1",
            model="Модель A",
            release_date=date(2023, 1, 1),
            organization=self.entity,
        )

    def test_product_creation(self):
        """Проверяем данные на соответствие"""
        self.assertEqual(self.product.name, "Продукт 1")
        self.assertEqual(self.product.model, "Модель A")
        self.assertEqual(self.product.release_date, date(2023, 1, 1))
        self.assertEqual(self.product.organization, self.entity)

    def test_str_representation(self):
        """Проверяем метод представления str"""
        self.assertEqual(str(self.product), "Продукт 1 (Модель A, 2023-01-01)")
