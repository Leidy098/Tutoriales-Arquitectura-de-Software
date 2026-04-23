from django.urls import path
from tienda_app.api.views import CompraAPIView, ProductoListAPIView

from .views import CompraView, home

urlpatterns = [
    path('', home, name='home'),
    path('compra/<int:libro_id>/', CompraView.as_view(), name='compra'),
    path('api/v1/productos/', ProductoListAPIView.as_view(), name='api_productos'),
    path('api/v1/comprar/', CompraAPIView.as_view(), name='api_comprar'),
]
