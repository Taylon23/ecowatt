from django.urls import path
from . import views
from django.contrib.auth import views as AuthViews

urlpatterns = [
     path('login/', views.CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('logout/', AuthViews.LogoutView.as_view(), name="logout"),
    path('perfil/', views.perfil, name="perfil"),
    path('perfil/atualizar/', views.completar_perfil, name='completar-perfil'),
    path('tarefas-concluidas/', views.tarefas_concluidas, name='tarefas-concluidas'),
    path('historico-consumo/', views.historico_consumo, name='historico-consumo'),
    path('meus-equipamentos/', views.meus_equipamentos, name='meus-equipamentos'),
    path('economia/', views.pagina_economia, name='pagina-economia'),
    path('alterar-senha/', views.alterar_senha, name='alterar-senha'),
    path('deletar-conta/', views.deletar_conta, name='deletar-conta'),
]


