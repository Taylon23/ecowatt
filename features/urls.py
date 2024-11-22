from django.urls import path
from .views import calculo_consumo, listar_equipamentos

urlpatterns = [
    path('calculo-consumo/', calculo_consumo, name='calculo_consumo'),
    path('meus-equipamentos/', listar_equipamentos, name='listar-equipamentos'),
]