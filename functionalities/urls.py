from django.urls import path
from . import views

urlpatterns = [
    # URL para criar um novo equipamento
    path('equipamento-criar/', views.criar_equipamento, name='criar-equipamento'),

    # URL para listar os equipamentos de um estabelecimento
    path('estabelecimento/<int:estabelecimento_id>/equipamentos/',
         views.lista_equipamentos, name='listar-equipamentos'),

    # URL para editar um equipamento específico
    path('equipamento/<int:equipamento_id>/editar/',
         views.editar_equipamento, name='editar-equipamento'),

    # URL para excluir um equipamento específico
    path('equipamento/<int:equipamento_id>/excluir/',
         views.excluir_equipamento, name='excluir-equipamento'),

    # URL para criar um novo estabelecimento
    path('estabelecimento/criar/', views.criar_estabelecimento,
         name='criar-estabelecimento'),

    # URL para editar um estabelecimento específico
    path('estabelecimento/<int:estabelecimento_id>/editar/',
         views.editar_estabelecimento, name='editar-estabelecimento'),

    # URL para excluir um estabelecimento específico
    path('estabelecimento/<int:estabelecimento_id>/excluir/',
         views.excluir_estabelecimento, name='excluir-estabelecimento'),

    # URL para listar os estabelecimentos do usuário logado
    path('meus-estabelecimentos/', views.lista_estabelecimentos,
         name='listar-estabelecimentos'),

    # URL para criar plano de economia
    path('criar-plano/', views.criar_plano_economia,
         name='criar-plano-economia'),

    # URL para criar plano de economia pleo butao
    path('criar-plano-economia/<int:estabelecimento_id>/',
         views.butao_criar_plano_economia, name='butao-criar-plano-economia'),

    # URL para listar planos planos de economia
    path('listar-planos/', views.listar_planos, name='listar-planos-economia'),

    # URL para editar plano específico
    path('planos/editar/<int:id>/', views.editar_plano, name='editar-plano'),

    # URL para excluir um plano específico
    path('planos/excluir/<int:id>/', views.excluir_plano, name='excluir-plano'),

    # URL para ordenar planos
    path('salvar-ordem/', views.salvar_ordem, name='salvar_ordem'),

    # URL para exibir grafico do plano
    path('plano/<int:plano_id>/grafico/',
         views.exibir_plano_grafico, name='ver-plano-grafico'),

    # URL para gerar dicas e solucao
    path('estabelecimento/<int:estabelecimento_id>/dicas/',
         views.dicas_economia, name='dicas-economia'),
]
