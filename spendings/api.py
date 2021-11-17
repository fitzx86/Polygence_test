from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from . import models as spendings_m
from . import serializers as spendings_ser


class SpendingModelViewSet(viewsets.ModelViewSet):
    queryset = spendings_m.Spending.objects.all()
    serializer_class = spendings_ser.SpendingSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['currency']
