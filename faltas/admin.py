from django.contrib import admin
from .models import FaltaAbonada


class FaltaAbonadaAdmin(admin.ModelAdmin):
    pass


admin.site.register(FaltaAbonada, FaltaAbonadaAdmin)
