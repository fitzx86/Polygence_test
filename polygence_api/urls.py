from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from spendings import api as spendings_api

api_router = routers.DefaultRouter()
api_router.register(r'spendings', spendings_api.SpendingModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include((api_router.urls, 'api')), name='api'),
]
