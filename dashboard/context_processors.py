from .models import UserEquipamento, Desafio, UserDesafio, PerfilGamer

def dados_dashboard(request):
    if request.user.is_authenticated:
        user_equipamentos = UserEquipamento.objects.filter(
            user=request.user).values_list('equipamento', flat=True)

        desafios = Desafio.objects.filter(
            equipamentos__in=user_equipamentos).distinct()

        desafios_nao_concluidos = []
        for desafio in desafios:
            user_desafio, created = UserDesafio.objects.get_or_create(
                user=request.user,
                desafio=desafio
            )
            if not user_desafio.completo:
                desafios_nao_concluidos.append(desafio)

        perfil, created = PerfilGamer.objects.get_or_create(user=request.user)
        pontuacao_atual = perfil.experiencia
        patente = perfil.get_patente_display()

        return {
            'desafios': desafios_nao_concluidos,
            'pontuacao_atual': pontuacao_atual,
            'patente': patente
        }
    return {}
