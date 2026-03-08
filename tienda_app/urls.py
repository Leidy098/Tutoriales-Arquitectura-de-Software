from django.urls import path
from .views import CompraView, home

urlpatterns = [
    path('', home, name='home'),
    path('compra/<int:libro_id>/', CompraView.as_view(), name='compra'),
]
