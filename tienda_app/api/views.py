from typing import TypedDict, cast

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tienda_app.infra.factories import PaymentFactory
from tienda_app.services import CompraService

from .serializers import OrdenInputSerializer


class OrdenInputData(TypedDict):
    libro_id: int
    direccion_envio: str


class CompraAPIView(APIView):
    """
    Endpoint para procesar compras via JSON.
    POST /api/comprar/
    Payload: { "libro_id": 1, "direccion_envio": "Calle 123" }
    """

    def post(self, request):
        serializer = OrdenInputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        datos = cast(OrdenInputData, serializer.validated_data)

        if not request.user.is_authenticated:
            return Response(
                {"error": "Debes iniciar sesion para comprar."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            gateway = PaymentFactory.get_processor()
            servicio = CompraService(procesador_pago=gateway)

            mensaje, estado = servicio.procesar_seguro(
                usuario=request.user,
                libro_id=datos["libro_id"],
                direccion=datos["direccion_envio"],
            )

            if estado == 200:
                return Response(
                    {"estado": "exito", "mensaje": mensaje},
                    status=status.HTTP_201_CREATED,
                )

            if estado == 404:
                return Response({"error": mensaje}, status=status.HTTP_404_NOT_FOUND)

            return Response({"error": mensaje}, status=status.HTTP_400_BAD_REQUEST)

        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_409_CONFLICT)
        except Exception:
            return Response(
                {"error": "Error interno"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
