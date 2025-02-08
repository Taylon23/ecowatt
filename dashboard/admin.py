from django.contrib import admin
from .models import Equipamento,Desafio, UserEquipamento,UserDesafio,PerfilGamer,Trofeu

    
admin.site.register(Equipamento)
admin.site.register(Desafio)
admin.site.register(UserEquipamento)
admin.site.register(UserDesafio)
admin.site.register(PerfilGamer)
admin.site.register(Trofeu)


