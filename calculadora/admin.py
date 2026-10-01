from django.contrib import admin

from .models import Calculo

admin.site.site_header = "Calculadora - administracao"


@admin.register(Calculo)
class CalculoAdmin(admin.ModelAdmin):
    list_display = ("x", "operacao", "y", "resultado", "criado_em")
    list_filter = ("operacao",)
    search_fields = ("resultado",)
