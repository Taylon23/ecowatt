import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Equipamento, Desafio, UserEquipamento, UserDesafio, PerfilGamer
from .forms import EquipamentoForm


@login_required
def selecionar_equipamentos(request):
    equipamentos = Equipamento.objects.all()  # Recupera todos os equipamentos
    return render(request, 'selecionar_equipamentos.html', {'equipamentos': equipamentos})


@login_required
def dashboard(request):
    # Recupera os IDs dos equipamentos do usuário
    user_equipamentos = UserEquipamento.objects.filter(
        user=request.user).values_list('equipamento', flat=True)

    # Filtra os desafios relacionados aos equipamentos do usuário
    desafios = Desafio.objects.filter(
        equipamentos__in=user_equipamentos).distinct()

    # Filtra os desafios que o usuário ainda não completou
    desafios_nao_concluidos = []
    for desafio in desafios:
        user_desafio, created = UserDesafio.objects.get_or_create(
            user=request.user,
            desafio=desafio
        )
        if not user_desafio.completo:
            desafios_nao_concluidos.append(desafio)

    # Recupera o perfil do usuário e a pontuação atual
    perfil, created = PerfilGamer.objects.get_or_create(user=request.user)
    pontuacao_atual = perfil.experiencia

    # Renderiza o template com os desafios e o perfil
    return render(request, 'dashboard.html', {
        'desafios': desafios_nao_concluidos,
        'pontuacao_atual': pontuacao_atual,
        'perfil': perfil  # <-- Adicionado aqui
    })


@login_required
@csrf_exempt
def salvar_equipamentos(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        equipamentos_ids = data.get('equipamentos', [])

        # Limpa equipamentos anteriores do usuário
        UserEquipamento.objects.filter(user=request.user).delete()

        # Salva os novos equipamentos selecionados
        for equipamento_id in equipamentos_ids:
            equipamento = Equipamento.objects.get(id=equipamento_id)
            UserEquipamento.objects.create(
                user=request.user, equipamento=equipamento)

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def detalhes_desafio(request, desafio_id):
    # Obtém o desafio pelo ID ou retorna um erro 404 se não existir
    desafio = get_object_or_404(Desafio, id=desafio_id)

    # Obtém ou cria uma entrada UserDesafio para o usuário logado
    user_desafio, created = UserDesafio.objects.get_or_create(
        user=request.user,
        desafio=desafio
    )

    # Renderiza o template com os detalhes do desafio e o status de conclusão
    return render(request, 'desafio_detail.html', {
        'desafio': desafio,
        'user_desafio': user_desafio,
    })


@login_required
def concluir_passo(request, desafio_id):
    user_desafio = get_object_or_404(
        UserDesafio, user=request.user, desafio_id=desafio_id)

    # Verifica se o perfil do usuário existe
    perfil, created = PerfilGamer.objects.get_or_create(user=request.user)

    user_desafio.concluir_passo()
    return redirect('detalhes-desafio', desafio_id=desafio_id)


@login_required
def marcar_desafio_completo(request, desafio_id):
    desafio = get_object_or_404(Desafio, id=desafio_id)
    user_desafio, created = UserDesafio.objects.get_or_create(
        user=request.user,
        desafio=desafio
    )
    user_desafio.completo = True
    user_desafio.save()
    return redirect('detalhes-desafio', desafio_id=desafio.id)
