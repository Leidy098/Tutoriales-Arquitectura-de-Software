from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from .services import CompraService
from .infra.factories import PaymentFactory

class CompraView(View):
    template_name = 'tienda_app/compra_rapida.html'
    service = CompraService(procesador_pago=PaymentFactory.get_processor())
    def get(self, request, libro_id): return render(request, self.template_name, self.service.obtener_contexto_seguro(libro_id))
    def post(self, request, libro_id):
        if not request.user.is_authenticated:
            return HttpResponse("Debes iniciar sesion para comprar.", status=401)

        direccion = request.POST.get('direccion', '').strip()
        mensaje, estado = self.service.procesar_seguro(request.user, libro_id, direccion)
        return HttpResponse(mensaje, status=estado)

def home(request):
    return render(request, 'tienda_app/home.html')
