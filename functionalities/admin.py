from django.contrib import admin
from . import models

admin.site.register(models.Equipamento)
admin.site.register(models.Estabelecimento)
admin.site.register(models.PlanoEconomia)
admin.site.register(models.Ajuste)


