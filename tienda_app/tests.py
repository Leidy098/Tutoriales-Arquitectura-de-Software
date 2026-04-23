from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tienda_app.models import Inventario, Libro


class ProductoListAPITests(APITestCase):
    def test_lista_productos_retorna_libros_con_stock(self):
        libro = Libro.objects.create(titulo="DDD Practico", precio="49.90")
        Inventario.objects.create(libro=libro, cantidad=7)

        response = self.client.get(reverse("api_productos"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["titulo"], "DDD Practico")
        self.assertEqual(response.data[0]["stock_actual"], 7)
