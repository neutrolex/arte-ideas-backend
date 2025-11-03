"""
URLs del Commerce App - Arte Ideas
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'commerce'

# Router para ViewSets
router = DefaultRouter()

urlpatterns = [
    # API Router
    path('', include(router.urls)),
]