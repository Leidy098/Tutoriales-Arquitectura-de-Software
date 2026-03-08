from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from .services import CompraRapidaService
from .infra.gateways import BancoNacionalProcesador

class CompraRapidaView(View):
    template_name = 'tienda_app/compra_rapida.html'
    service = CompraRapidaService(procesador_pago=BancoNacionalProcesador())
    def get(self, request, libro_id): return render(request, self.template_name, self.service.obtener_contexto_seguro(libro_id))
    def post(self, request, libro_id):
        mensaje, estado = self.service.procesar_seguro(libro_id)
        return HttpResponse(mensaje, status=estado)

def home(request):
    return render(request, 'tienda_app/home.html')