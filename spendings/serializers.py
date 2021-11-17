from rest_framework import serializers
from . import models as spendings_m


class SpendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = spendings_m.Spending
        fields = '__all__'
