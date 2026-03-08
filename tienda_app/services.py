from .models import Libro, Inventario
from .domain.logic import CalculadorImpuestos
from .domain.builders import OrdenBuilder


class CompraService:
    def __init__(self, procesador_pago):
        self.procesador = procesador_pago
        self.builder = OrdenBuilder()

    def ejecutar_proceso_compra(self, usuario, lista_productos, direccion):
        # Uso del Builder: Semantica clara y validacion interna.
        orden = (
            self.builder
            .con_usuario(usuario)
            .con_productos(lista_productos)
            .para_envio(direccion)
            .build()
        )

        # Uso del Factory (inyectado): cambio de comportamiento sin cambio de codigo.
        if self.procesador.pagar(orden.total):
            return f"Orden {orden.id} procesada exitosamente."

        orden.delete()
        raise Exception("Error en la pasarela de pagos.")

    def obtener_detalle_producto(self, libro_id):
        libro = Libro.objects.get(id=libro_id)
        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)
        return {"libro": libro, "total": total}

    def obtener_contexto_seguro(self, libro_id):
        try:
            return self.obtener_detalle_producto(libro_id)
        except Libro.DoesNotExist:
            return {"error": "Producto no disponible"}

    def procesar_seguro(self, usuario, libro_id, direccion):
        try:
            libro = Libro.objects.get(id=libro_id)
            inventario = Inventario.objects.get(libro=libro)

            if inventario.cantidad <= 0:
                return "No hay existencias.", 400

            mensaje = self.ejecutar_proceso_compra(
                usuario=usuario,
                lista_productos=[libro],
                direccion=direccion,
            )

            inventario.cantidad -= 1
            inventario.save()
            return mensaje, 200
        except (Libro.DoesNotExist, Inventario.DoesNotExist):
            return "Producto no disponible", 404
        except ValueError as e:
            return str(e), 400
        except Exception as e:
            return str(e), 400
