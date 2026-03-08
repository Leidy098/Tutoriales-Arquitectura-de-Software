from .models import Libro, Inventario
from .domain.logic import CalculadorImpuestos


class CompraRapidaService:
    def __init__(self, procesador_pago):
        self.procesador_pago = procesador_pago

    def obtener_detalle_producto(self, libro_id):
        libro = Libro.objects.get(id=libro_id)
        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)
        return {"libro": libro, "total": total}

    def procesar(self, libro_id):
        libro = Libro.objects.get(id=libro_id)
        inv = Inventario.objects.get(libro=libro)

        if inv.cantidad <= 0:
            raise ValueError("No hay existencias.")

        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)

        if self.procesador_pago.pagar(total):
            inv.cantidad -= 1
            inv.save()

            return total

        return None

    def obtener_contexto_seguro(self, libro_id):
        try:
            return self.obtener_detalle_producto(libro_id)
        except Libro.DoesNotExist:
            return {"error": "Producto no disponible"}

    def procesar_seguro(self, libro_id):
        try:
            total = self.procesar(libro_id)
        except (Libro.DoesNotExist, Inventario.DoesNotExist):
            return "Producto no disponible", 404
        except ValueError as e:
            return str(e), 400

        if total is None:
            return "Error", 400

        return f"Comprado via CBV: ${total}", 200
