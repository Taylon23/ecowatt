from .models import UserEquipamento, Tarefa, UserTarefa, PerfilGamer

def dados_dashboard(request):
    if request.user.is_authenticated:
        perfil, created = PerfilGamer.objects.get_or_create(user=request.user)
        pontuacao_atual = perfil.experiencia
        patente = perfil.get_patente_display()

        return {
            'pontuacao_atual': pontuacao_atual,
            'patente': patente
        }
    return {}
