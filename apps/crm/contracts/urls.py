from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContractViewSet

app_name = 'contracts'

router = DefaultRouter()
router.register(r'', ContractViewSet, basename='contracts')

urlpatterns = [
    path('', include(router.urls)),
]