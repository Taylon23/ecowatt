from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('selecionar-equipamentos/', views.selecionar_equipamentos,
         name='selecionar-equipamentos'),
    path('salvar-equipamentos/', views.salvar_equipamentos,
         name='salvar-equipamentos'),
    path('desafio/<int:desafio_id>/',
         views.detalhes_desafio, name='detalhes-desafio'),
    path('desafio/<int:desafio_id>/concluir-passo/',
         views.concluir_passo, name='concluir-passo'),
    path('desafio/<int:desafio_id>/completo/',
         views.marcar_desafio_completo, name='marcar-desafio-completo'),
]
