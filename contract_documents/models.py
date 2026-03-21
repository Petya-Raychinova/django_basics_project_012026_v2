from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from bonuspercent.models import ConditionsPercent


def validate_file_size(file):
    max_size = 5 * 1024 * 1024  # 5 MB
    if file.size > max_size:
        raise ValidationError("Файлът за качване трябва да бъде до 5MB.")


class ContractDocument(models.Model):

    supplier = models.ForeignKey(
        ConditionsPercent,
        on_delete=models.CASCADE
    )

    document = models.FileField(
        upload_to="contracts/",
        validators=[
            FileExtensionValidator(allowed_extensions=["pdf"]),
            validate_file_size
        ]
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    description = models.CharField(
        max_length=255,
        blank=True
    )

    def __str__(self):
        return f"Contract for {self.supplier.eik}"
