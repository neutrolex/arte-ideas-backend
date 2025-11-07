from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'inventario'

# Router para ViewSets
router = DefaultRouter()
router.register(r'moldura-liston', views.MolduraListonViewSet)
router.register(r'moldura-prearmada', views.MolduraPrearmadaViewSet)
router.register(r'vidrio-tapa-mdf', views.VidrioTapaMDFViewSet)
router.register(r'paspartu', views.PaspartuViewSet)
router.register(r'minilab', views.MinilabViewSet)
router.register(r'cuadro', views.CuadroViewSet)
router.register(r'anuario', views.AnuarioViewSet)
router.register(r'corte-laser', views.CorteLaserViewSet)
router.register(r'marco-accesorio', views.MarcoAccesorioViewSet)
router.register(r'herramienta-general', views.HerramientaGeneralViewSet)

urlpatterns = [
    # API Router
    path('api/', include(router.urls)),
    # Endpoints específicos
    path('api/dashboard/', views.dashboard_inventario, name='dashboard_api'),
    path('api/metricas/', views.metricas_api, name='metricas_api'),
]