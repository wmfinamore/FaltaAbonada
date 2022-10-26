from django.views.generic import ListView
from .models import FaltaAbonada


class FaltasListView(ListView):
    model = FaltaAbonada
    context_object_name = 'faltas_abonadas'
