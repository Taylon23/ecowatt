from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('selecionar-equipamentos/', views.selecionar_equipamentos,
         name='selecionar-equipamentos'),
    path('salvar-equipamentos/', views.salvar_equipamentos,
         name='salvar-equipamentos'),
    path('tarefa/<int:tarefa_id>/',
         views.detalhes_tarefa, name='detalhes-tarefa'),
    path('tarefa/<int:tarefa_id>/concluir-passo/',
         views.concluir_passo, name='concluir-passo'),
    path('tarefa/<int:tarefa_id>/completo/',
         views.marcar_desafio_completo, name='marcar-tarefa-completo'),
    path('configuracoes',views.configuracoes, name='configuracoes'),

]
