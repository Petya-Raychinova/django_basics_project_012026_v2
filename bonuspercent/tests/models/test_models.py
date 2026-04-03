from django.test import TestCase
from bonuspercent.models import (
    ProductCategory,
    ConditionsPercent,
    PurchasingAmount,
    PaymentTerm
)


class ProductCategoryTests(TestCase):

    def test_create_category_expect_success(self):
        # Arrange
        category_name = "Food"

        # Act
        # валидира създаването на запис в модела ProductCategory и правилното записване на стойността
        category = ProductCategory.objects.create(
            product_category_name=category_name
        )

        # Assert
        self.assertEqual(category.product_category_name, category_name)

    def test_category_str_expect_name(self):
        # Arrange
        category = ProductCategory.objects.create(
            product_category_name="Drinks"
        )

        # Act
        # дали връща името на категорията
        result = str(category)

        # Assert
        self.assertEqual(result, "Drinks")


class PaymentTermTests(TestCase):

    def test_create_payment_term_expect_success(self):
        # Arrange
        name = "Net 30"
        days = 30

        # Act
        # валидира, че се създава с коректни стойности
        term = PaymentTerm.objects.create(
            name=name,
            days=days
        )

        # Assert
        self.assertEqual(term.days, days)

    def test_payment_term_str_expect_correct_format(self):
        # Arrange
        term = PaymentTerm.objects.create(
            name="Net 15",
            days=15
        )

        # Act
        # дали форматира правилно
        result = str(term)

        # Assert
        self.assertEqual(result, "Net 15 (15 дни)")


class ConditionsPercentTests(TestCase):

    def setUp(self):
        self.category = ProductCategory.objects.create(
            product_category_name="Food"
        )
        self.payment_term = PaymentTerm.objects.create(
            name="Net 30",
            days=30
        )

    def test_create_condition_expect_success(self):
        # Arrange
        eik = "1234567890"

        # Act
        # валидира създаването на доставчик с уникален ЕИК
        condition = ConditionsPercent.objects.create(
            eik=eik,
            supplier_name="Supplier A",
            percent_condition=10.50
        )

        # Assert
        self.assertEqual(condition.eik, eik)

    def test_condition_str_expect_correct_format(self):
        # Arrange
        condition = ConditionsPercent.objects.create(
            eik="1234567891",
            supplier_name="Supplier B",
            percent_condition=5
        )

        # Act
        # формат
        result = str(condition)

        # Assert
        self.assertEqual(result, "Supplier B (5.00)")

    def test_add_category_expect_success(self):
        # Arrange
        condition = ConditionsPercent.objects.create(
            eik="1234567892",
            supplier_name="Supplier C",
            percent_condition=7
        )

        # Act
        # vалидира, че към доставчик могат да се добавят категории чрез many-to-many връзка
        condition.categories.add(self.category)

        # Assert
        self.assertEqual(condition.categories.count(), 1)

    def test_add_payment_term_expect_success(self):
        # Arrange
        condition = ConditionsPercent.objects.create(
            eik="1234567893",
            supplier_name="Supplier D",
            percent_condition=8
        )

        # Act
        # свързани условия за плащане
        condition.payment_terms.add(self.payment_term)

        # Assert
        self.assertEqual(condition.payment_terms.count(), 1)

    def test_duplicate_eik_expect_failure(self):
        # Arrange
        ConditionsPercent.objects.create(
            eik="1234567894",
            supplier_name="Supplier E",
            percent_condition=10
        )

        # Act & Assert
        # гарантира, че не могат да се създават два доставчика седин и същ ЕИК
        with self.assertRaises(Exception):
            ConditionsPercent.objects.create(
                eik="1234567894",
                supplier_name="Duplicate",
                percent_condition=5
            )


class PurchasingAmountTests(TestCase):

    def setUp(self):
        self.condition = ConditionsPercent.objects.create(
            eik="1234567895",
            supplier_name="Supplier F",
            percent_condition=12
        )

    def test_create_purchase_expect_success(self):
        # Arrange
        amount = 1000

        # Act
        # валидира запис на стойност за покупка към доставчик
        purchase = PurchasingAmount.objects.create(
            condition_eik=self.condition,
            purchasing_amount=amount
        )

        # Assert
        self.assertEqual(purchase.purchasing_amount, amount)

    def test_foreign_key_relation_expect_correct_eik(self):
        # Arrange
        purchase = PurchasingAmount.objects.create(
            condition_eik=self.condition,
            purchasing_amount=500
        )

        # Act
        # проверява връзката между покупка и доставчик чрез foreign key
        result = purchase.condition_eik.eik

        # Assert
        self.assertEqual(result, "1234567895")

    def test_purchase_str_expect_contains_eik(self):
        # Arrange
        purchase = PurchasingAmount.objects.create(
            condition_eik=self.condition,
            purchasing_amount=250
        )

        # Act
        # дали съдържаЕИК на доставчика
        result = str(purchase)

        # Assert
        self.assertIn("1234567895", result)