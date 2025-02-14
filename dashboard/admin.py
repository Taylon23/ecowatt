from django.contrib import admin
from .models import Equipamento,Tarefa, UserEquipamento,UserTarefa,PerfilGamer,TextoDicas

    
admin.site.register(Equipamento)
admin.site.register(Tarefa)
admin.site.register(UserEquipamento)
admin.site.register(UserTarefa)
admin.site.register(PerfilGamer)
admin.site.register(TextoDicas)
