from django.urls import path
from .views import FaltasListView
from django.views.decorators.cache import cache_page
from config.settings import CACHE_TIME


urlpatterns = [
    path('', cache_page(CACHE_TIME * 1)(FaltasListView.as_view()), name='lista_faltas'),
]
