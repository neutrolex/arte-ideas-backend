from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContratoViewSet

app_name = 'contracts'

router = DefaultRouter()
router.register(r'', ContratoViewSet, basename='contratos')

urlpatterns = [
    path('', include(router.urls)),
]