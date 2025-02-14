import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Equipamento, Tarefa, UserEquipamento, UserTarefa, PerfilGamer
from .forms import EquipamentoForm


@login_required
def selecionar_equipamentos(request):
    equipamentos = Equipamento.objects.all()  # Recupera todos os equipamentos
    user_equipamentos = UserEquipamento.objects.filter(user=request.user).values_list(
        'equipamento_id', flat=True)  # IDs dos equipamentos já selecionados
    return render(request, 'selecionar_equipamentos.html', {
        'equipamentos': equipamentos,
        # Passa os IDs para o template
        'user_equipamentos': list(user_equipamentos)
    })


@login_required
def dashboard(request):
    if request.user.is_authenticated:
        # Filtra os equipamentos do usuário
        user_equipamentos = UserEquipamento.objects.filter(
            user=request.user
        ).values_list('equipamento', flat=True)

        # Filtra as tarefas relacionadas aos equipamentos do usuário
        tarefas = Tarefa.objects.filter(
            equipamentos__in=user_equipamentos
        ).distinct()

        # Filtra as tarefas não concluídas pelo usuário
        tarefas_nao_concluidas = []
        for tarefa in tarefas:
            user_tarefa, created = UserTarefa.objects.get_or_create(
                user=request.user,
                tarefa=tarefa
            )
            if not user_tarefa.completo:
                # Adiciona a instância de Tarefa
                tarefas_nao_concluidas.append(tarefa)

    return render(request, 'dashboard.html', {'tarefas': tarefas_nao_concluidas})


@login_required
@csrf_exempt
def salvar_equipamentos(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        equipamentos_ids = data.get('equipamentos', [])

        # Salva os novos equipamentos selecionados
        for equipamento_id in equipamentos_ids:
            equipamento = Equipamento.objects.get(id=equipamento_id)
            UserEquipamento.objects.update_or_create(
                user=request.user,
                equipamento=equipamento,
                # Atualiza ou cria o registro
                defaults={'equipamento': equipamento}
            )

        # Remove equipamentos que não foram selecionados
        UserEquipamento.objects.filter(user=request.user).exclude(
            equipamento_id__in=equipamentos_ids).delete()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def detalhes_tarefa(request, tarefa_id):
    # Obtém o desafio pelo ID ou retorna um erro 404 se não existir
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)

    # Obtém ou cria uma entrada UserTarefa para o usuário logado
    user_tarefa, created = UserTarefa.objects.get_or_create(
        user=request.user,
        tarefa=tarefa
    )

    # Renderiza o template com os detalhes do desafio e o status de conclusão
    return render(request, 'tarefas_detail.html', {
        'tarefa': tarefa,
        'user_tarefa': user_tarefa,
    })


@login_required
def concluir_passo(request, tarefa_id):
    user_tarefa = get_object_or_404(
        UserTarefa, user=request.user, tarefa_id=tarefa_id)

    # Verifica se o perfil do usuário existe
    perfil, created = PerfilGamer.objects.get_or_create(user=request.user)

    user_tarefa.concluir_passo()
    return redirect('detalhes-tarefa', tarefa_id=tarefa_id)


@login_required
def marcar_desafio_completo(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    user_tarefa, created = UserTarefa.objects.get_or_create(
        user=request.user,
        tarefa=tarefa
    )
    user_tarefa.completo = True
    user_tarefa.save()
    return redirect('detalhes-tarefa', tarefa_id=tarefa.id)


@login_required
def configuracoes(request):
    return render(request, 'configuracoes.html')
