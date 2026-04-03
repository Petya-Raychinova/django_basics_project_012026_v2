from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from bonuspercent.models import ConditionsPercent, PurchasingAmount

User = get_user_model()


class IndexViewTests(TestCase):

    def setUp(self):
        # Създаваме user- защото view-то е защитено
        self.user = User.objects.create_user(
            email="test@test.com",
            password="12345678"
        )
        # дали страницата се отваря
    def test_index_view_not_logged_expect_redirect(self):
        # Act
        response = self.client.get(reverse("bonuspercent:index"))

        # Assert
        self.assertEqual(response.status_code, 302)

    def test_index_view_logged_expect_success(self):
        # Arrange
        self.client.login(email="test@test.com", password="12345678")

        # Act
        response = self.client.get(reverse("bonuspercent:index"))

        # Assert
        self.assertEqual(response.status_code, 200)


class BonusReportViewTests(TestCase):

    def setUp(self):
        self.condition = ConditionsPercent.objects.create(
            eik="1234567890",
            supplier_name="Supplier",
            percent_condition=10
        )

        PurchasingAmount.objects.create(
            condition_eik=self.condition,
            purchasing_amount=100
        )

    def test_bonus_report_view_expect_success(self):
        # Act
        response = self.client.get(reverse("bonuspercent:bonus_report")) # съдържа данни

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Supplier")


class SupplierViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            password="12345678"
        )

        self.condition = ConditionsPercent.objects.create(
            eik="1234567891",
            supplier_name="Supplier A",
            percent_condition=10
        )

    def test_supplier_list_expect_success(self):
        # Act
        response = self.client.get(reverse("bonuspercent:supplier_list_sorted")) # списък

        # Assert
        self.assertEqual(response.status_code, 200)

    def test_supplier_edit_post_expect_redirect(self):
        # Arrange
        self.client.login(email="test@test.com", password="12345678")

        form_data = {
            "eik": "1234567891",
            "supplier_name": "Updated",
            "percent_condition": 20,
        }

        # Act
        # POST дали работи
        response = self.client.post(
            reverse("bonuspercent:supplier_edit", args=[self.condition.id]),
            data=form_data
        )

        # Assert
        self.assertEqual(response.status_code, 302)

    def test_supplier_delete_post_expect_redirect(self):
        # Arrange
        self.client.login(email="test@test.com", password="12345678")

        # Act
        # дали изтрива
        response = self.client.post(
            reverse("bonuspercent:supplier_delete", args=[self.condition.id])
        )

        # Assert
        self.assertEqual(response.status_code, 302)


class PurchaseViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            password="12345678"
        )

        self.condition = ConditionsPercent.objects.create(
            eik="1234567892",
            supplier_name="Supplier",
            percent_condition=10
        )

        self.purchase = PurchasingAmount.objects.create(
            condition_eik=self.condition,
            purchasing_amount=100
        )

    def test_purchase_list_expect_success(self):
        # Act
        response = self.client.get(reverse("bonuspercent:purchase_list_sorted"))

        # Assert
        self.assertEqual(response.status_code, 200)

    def test_purchase_edit_post_expect_redirect(self):
        # Arrange
        self.client.login(email="test@test.com", password="12345678")

        form_data = {
            "condition_eik": self.condition.id,
            "purchasing_amount": 200,
        }

        # Act
        response = self.client.post(
            reverse("bonuspercent:purchase_edit", args=[self.purchase.id]),
            data=form_data
        )

        # Assert
        self.assertEqual(response.status_code, 302)

    def test_purchase_delete_post_expect_redirect(self):
        # Arrange
        self.client.login(email="test@test.com", password="12345678")

        # Act
        response = self.client.post(
            reverse("bonuspercent:purchase_delete", args=[self.purchase.id])
        )

        # Assert
        self.assertEqual(response.status_code, 302)