from .models import PerfilGamer
from .choices import DESCRICOES_PATENTES  # Importe o dicionário de descrições

def dados_dashboard(request):
    if request.user.is_authenticated:
        perfil, created = PerfilGamer.objects.get_or_create(user=request.user)
        pontuacao_atual = perfil.experiencia
        patente = perfil.get_patente_display()
        
        # Obtém a descrição da patente atual
        descricao_patente = DESCRICOES_PATENTES.get(perfil.patente, "Descrição não disponível.")

        return {
            'pontuacao_atual': pontuacao_atual,
            'patente': patente,
            'descricao_patente': descricao_patente  # Adiciona a descrição ao contexto
        }
    return {}