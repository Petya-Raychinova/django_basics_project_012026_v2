from django.test import TestCase
from bonuspercent.forms import ConditionForm, PurchasingForm
from bonuspercent.models import ConditionsPercent


class ConditionFormTests(TestCase):

    def test_condition_form_valid_data_expect_success(self):
        # Arrange
        form_data = {
            "eik": "1234567890",
            "supplier_name": "Test Supplier",
            "percent_condition": 10,
        }

        # Act
        # дали формата приема коректни данни
        form = ConditionForm(data=form_data)

        # Assert
        self.assertTrue(form.is_valid())

    def test_condition_form_invalid_eik_letters_expect_failure(self):
        # Arrange
        form_data = {
            "eik": "abc123",
            "supplier_name": "Test Supplier",
            "percent_condition": 10,
        }

        # Act
        # EIK не може да съдържа букви
        form = ConditionForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())

    def test_condition_form_invalid_eik_length_expect_failure(self):
        # Arrange
        form_data = {
            "eik": "123",
            "supplier_name": "Test Supplier",
            "percent_condition": 10,
        }

        # Act
        # EIK трябва да е между 10 и 13 цифри
        form = ConditionForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())

    def test_condition_form_duplicate_eik_expect_failure(self):
        # Arrange
        ConditionsPercent.objects.create(
            eik="1234567891",
            supplier_name="Existing",
            percent_condition=10
        )

        form_data = {
            "eik": "1234567891",
            "supplier_name": "Duplicate",
            "percent_condition": 20,
        }

        # Act
        # не може да има два доставчика със същия EIK
        form = ConditionForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())

    def test_condition_form_invalid_supplier_name_expect_failure(self):
        # Arrange
        form_data = {
            "eik": "1234567892",
            "supplier_name": "Test123",  # съдържа цифри
            "percent_condition": 10,
        }

        # Act
        form = ConditionForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())

    def test_condition_form_negative_percent_expect_failure(self):
        # Arrange
        form_data = {
            "eik": "1234567893",
            "supplier_name": "Test Supplier",
            "percent_condition": -5, # отрицателно число
        }

        # Act
        form = ConditionForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())

    def test_condition_form_percent_over_100_expect_failure(self):
        # Arrange
        form_data = {
            "eik": "1234567894",
            "supplier_name": "Test Supplier",
            "percent_condition": 150, # стойност над 100
        }

        # Act
        form = ConditionForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())


class PurchasingFormTests(TestCase):

    def setUp(self):
        self.condition = ConditionsPercent.objects.create(
            eik="1234567895",
            supplier_name="Supplier",
            percent_condition=10
        )

    def test_purchasing_form_valid_data_expect_success(self):
        # Arrange
        form_data = {
            "condition_eik": self.condition.id,
            "purchasing_amount": 1000,
        }

        # Act
        # приема валидни данни за покупка
        form = PurchasingForm(data=form_data)

        # Assert
        self.assertTrue(form.is_valid())

    def test_purchasing_form_missing_amount_expect_failure(self):
        # Arrange
        form_data = {
            "condition_eik": self.condition.id,
        }

        # Act
        # задължителна стойност
        form = PurchasingForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())