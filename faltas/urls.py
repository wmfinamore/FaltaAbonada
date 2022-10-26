from django.urls import path
from .views import FaltasListView


urlpatterns = [
    path('', FaltasListView.as_view(), name='lista_faltas'),
]
