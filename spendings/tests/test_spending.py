import pytest
import json
import decimal
from django.urls import reverse
from django.test import Client
from spendings.models import Spending

client = Client()


@pytest.fixture
def test_data():
    test_data = {"amount": decimal.Decimal('15.00'), "currency": "USD"}
    return Spending.objects.create(**test_data)


@pytest.mark.django_db
def test_spending_create(test_data):
    assert Spending.objects.count() == 1


@pytest.mark.django_db
def test_spending_api_list(test_data):
    response = client.get(reverse('api:spending-list'))
    assert len(response.data) == Spending.objects.count()
    assert response.data[0]['amount'] == str(test_data.amount)


@pytest.mark.django_db
def test_spending_api_post(test_data):
    post_data = {"amount": "12.00", "currency": "HUF"}
    client.post(reverse('api:spending-list'), json.dumps(post_data),
                content_type="application/json")
    assert Spending.objects.count() == 2


@pytest.mark.django_db
def test_spending_api_update(test_data):
    post_data = {"amount": "19.00", "currency": "NOK"}
    url = reverse('api:spending-list') + str(test_data.id) + "/"
    client.put(url, json.dumps(post_data),
               content_type="application/json")
    test_obj = Spending.objects.get(pk=test_data.pk)
    assert test_obj.currency == "NOK"
    assert test_obj.amount == decimal.Decimal('19.00')


@pytest.mark.django_db
def test_spending_api_partial_update(test_data):
    post_data = {"amount": "19.00"}
    url = reverse('api:spending-list') + str(test_data.id) + "/"
    client.patch(url, json.dumps(post_data),
               content_type="application/json")
    test_obj = Spending.objects.get(pk=test_data.pk)
    assert test_obj.currency == "USD"
    assert test_obj.amount == decimal.Decimal('19.00')


@pytest.mark.django_db
def test_spending_api_delete(test_data):
    post_data = {"amount": "12.00", "currency": "HUF"}
    client.post(reverse('api:spending-list'), json.dumps(post_data),
                content_type="application/json")
    client.delete(reverse('api:spending-list') + str(test_data.id) + "/")
    assert Spending.objects.count() == 1


@pytest.mark.django_db
def test_spending_api_filter_currency(test_data):
    post_data = {"amount": "12.00", "currency": "HUF"}
    client.post(reverse('api:spending-list'), json.dumps(post_data),
                content_type="application/json")
    url = reverse('api:spending-list') + "?currency=HUF"
    response = client.get(url)
    assert Spending.objects.count() == 2
    assert len(response.data) == Spending.objects.filter(currency='HUF').count()


@pytest.mark.django_db
def test_spending_api_order_by_amount(test_data):
    post_data = {"amount": "12.00", "currency": "HUF"}
    client.post(reverse('api:spending-list'), json.dumps(post_data),
                content_type="application/json")
    url = reverse('api:spending-list') + "?ordered=-amount"
    response = client.get(url)
    assert Spending.objects.count() == 2
    assert response.data[0]['amount'] == "15.00"
    assert response.data[1]['amount'] == "12.00"
