from django.urls import path
from . import views

urlpatterns = [
    # URL para criar um novo equipamento
    path('equipamento-criar/', views.criar_equipamento, name='criar-equipamento'),

    # URL para listar os equipamentos de um estabelecimento
    path('estabelecimento/<int:estabelecimento_id>/equipamentos/', views.lista_equipamentos, name='listar-equipamentos'),

    # URL para editar um equipamento específico
    path('equipamento/<int:equipamento_id>/editar/', views.editar_equipamento, name='editar-equipamento'),

    # URL para excluir um equipamento específico
    path('equipamento/<int:equipamento_id>/excluir/', views.excluir_equipamento, name='excluir-equipamento'),

    # URL para criar um novo estabelecimento
    path('estabelecimento/criar/', views.criar_estabelecimento, name='criar-estabelecimento'),

    # URL para editar um estabelecimento específico
    path('estabelecimento/<int:estabelecimento_id>/editar/', views.editar_estabelecimento, name='editar-estabelecimento'),

    # URL para excluir um estabelecimento específico
    path('estabelecimento/<int:estabelecimento_id>/excluir/', views.excluir_estabelecimento, name='excluir-estabelecimento'),

    # URL para listar os estabelecimentos do usuário logado
    path('meus-estabelecimentos/', views.lista_estabelecimentos, name='listar-estabelecimentos'),
]
