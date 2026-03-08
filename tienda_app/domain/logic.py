from decimal import Decimal


class CalculadorImpuestos:
    """
    S: Responsabilidad única - Solo calcula impuestos.
    O: Abierto a extensión - Podríamos heredar para diferentes países.
    """
    @staticmethod
    def obtener_total_con_iva(precio_base) -> Decimal:
        iva = Decimal("1.19")  # Regla de negocio pura
        return Decimal(precio_base) * iva
