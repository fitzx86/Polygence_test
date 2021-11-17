from django.db import models
import moneyed


class Spending(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, choices=((code, currency.name) for code, currency in moneyed.CURRENCIES.items()))
    decription = models.TextField(blank=True)
