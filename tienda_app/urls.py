from django.urls import path
from .views import CompraRapidaView, home

urlpatterns = [
    path('', home, name='home'),
    path('compra-rapida/<int:libro_id>/', CompraRapidaView.as_view(), name='compra_rapida_cbv'),
]
