from rest_framework import serializers


class BonusReportSerializer(serializers.Serializer):
    eik = serializers.CharField()
    supplier_name = serializers.CharField()
    percent = serializers.DecimalField(max_digits=5, decimal_places=2)
    purchasing_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    bonus = serializers.DecimalField(max_digits=15, decimal_places=2)