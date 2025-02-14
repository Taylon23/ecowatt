from django.shortcuts import render
from .models import PerfilGamer, TextoDicas  # Importe o modelo TextoDicas
from .choices import DESCRICOES_PATENTES
import random  # Importe a função random

def dados_dashboard(request):
    context = {}
    if request.user.is_authenticated:
        perfil, created = PerfilGamer.objects.get_or_create(user=request.user)
        pontuacao_atual = perfil.experiencia
        patente = perfil.get_patente_display()
        
        # Obtém a descrição da patente atual
        descricao_patente = DESCRICOES_PATENTES.get(perfil.patente, "Descrição não disponível.")

        # Seleciona uma dica aleatória
        dicas = TextoDicas.objects.all()
        if dicas.exists():
            dica_aleatoria = random.choice(dicas)  # Seleciona uma dica aleatória
            context['dica_aleatoria'] = dica_aleatoria.texto

        context.update({
            'pontuacao_atual': pontuacao_atual,
            'patente': patente,
            'descricao_patente': descricao_patente,
        })

    return context