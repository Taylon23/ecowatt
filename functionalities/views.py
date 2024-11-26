from django.shortcuts import render, redirect, get_object_or_404
from .forms import CalculoConsumoForm, EstabelecimentoForm, PlanoEconomiaForm
from . import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import DicasEconomia
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def criar_equipamento(request):
    if request.method == 'POST':
        form = CalculoConsumoForm(request.POST)
        if form.is_valid():
            # Salva o equipamento com o usuário logado
            equipamento = form.save(commit=False)
            equipamento.user = request.user  # Associa o usuário logado
            equipamento.save()  # Salva no banco de dados

            # Adiciona uma mensagem de sucesso
            messages.success(request, "Equipamento cadastrado com sucesso!")

            # Redireciona para a página de listagem de equipamentos
            return redirect('listar-equipamentos', estabelecimento_id=equipamento.estabelecimento.id)

    else:
        form = CalculoConsumoForm()

    return render(request, 'calculo_consumo.html', {'form': form})


@login_required
def lista_equipamentos(request, estabelecimento_id):
    # Pega o estabelecimento específico
    estabelecimento = get_object_or_404(
        models.Estabelecimento, id=estabelecimento_id, user=request.user)

    # Pega os equipamentos relacionados a esse estabelecimento
    equipamentos = models.Equipamento.objects.filter(
        estabelecimento=estabelecimento)

    return render(request, 'listar_equipamentos.html', {'estabelecimento': estabelecimento, 'equipamentos': equipamentos})


@login_required
def editar_equipamento(request, equipamento_id):
    equipamento = get_object_or_404(
        models.Equipamento, id=equipamento_id, user=request.user)

    if request.method == 'POST':
        form = CalculoConsumoForm(request.POST, instance=equipamento)
        if form.is_valid():
            form.save()
            messages.success(request, "Equipamento atualizado com sucesso!")
            return redirect('listar-equipamentos', estabelecimento_id=equipamento.estabelecimento.id)
    else:
        form = CalculoConsumoForm(instance=equipamento)

    return render(request, 'editar-equipamento.html', {'form': form})


@login_required
def excluir_equipamento(request, equipamento_id):
    equipamento = get_object_or_404(
        models.Equipamento, id=equipamento_id, user=request.user)

    if request.method == 'POST':
        estabelecimento_id = equipamento.estabelecimento.id
        equipamento.delete()
        messages.success(request, "Equipamento excluído com sucesso!")
        return redirect('listar-equipamentos', estabelecimento_id=estabelecimento_id)

    return render(request, 'confirmar_exclusao_equipamento.html', {'equipamento': equipamento})

# CRUD para Estabelecimento


@login_required
def criar_estabelecimento(request):
    if request.method == 'POST':
        form = EstabelecimentoForm(request.POST)
        if form.is_valid():
            estabelecimento = form.save(commit=False)
            estabelecimento.user = request.user
            estabelecimento.save()

            messages.success(
                request, "Estabelecimento cadastrado com sucesso!")

            return redirect('listar-estabelecimentos')
    else:
        form = EstabelecimentoForm()
    return render(request, 'criar-estabelecimento.html', {'form': form})


@login_required
def lista_estabelecimentos(request):
    estabelecimento = models.Estabelecimento.objects.filter(user=request.user)

    return render(request, 'listar_estabelecimentos.html', {'estabelecimentos': estabelecimento})


@login_required
def editar_estabelecimento(request, estabelecimento_id):
    estabelecimento = get_object_or_404(
        models.Estabelecimento, id=estabelecimento_id, user=request.user)

    if request.method == 'POST':
        form = EstabelecimentoForm(request.POST, instance=estabelecimento)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Estabelecimento atualizado com sucesso!")
            return redirect('listar-estabelecimentos')
    else:
        form = EstabelecimentoForm(instance=estabelecimento)

    return render(request, 'editar-estabelecimento.html', {'form': form})


@login_required
def excluir_estabelecimento(request, estabelecimento_id):
    estabelecimento = get_object_or_404(
        models.Estabelecimento, id=estabelecimento_id, user=request.user)

    if request.method == 'POST':
        estabelecimento.delete()
        messages.success(request, "Estabelecimento excluído com sucesso!")
        return redirect('listar-estabelecimentos')

    return render(request, 'confirmar_exclusao_estabelecimento.html', {'estabelecimento': estabelecimento})


@login_required
def criar_plano_economia(request):
    if request.method == 'POST':
        form = PlanoEconomiaForm(request.POST)
        if form.is_valid():
            plano = form.save(commit=False)
            plano.user = request.user
            plano.save()
            return redirect('listar-planos-economia')
    else:
        form = PlanoEconomiaForm()
    return render(request, 'criar_plano_economia.html', {'form': form})


def butao_criar_plano_economia(request, estabelecimento_id):
    estabelecimento = get_object_or_404(
        models.Estabelecimento, id=estabelecimento_id, user=request.user)

    if request.method == "POST":
        form = PlanoEconomiaForm(request.POST)
        if form.is_valid():
            plano = form.save(commit=False)
            plano.estabelecimento = estabelecimento
            plano.user = request.user
            plano.save()
            messages.success(request, "Plano de economia criado com sucesso!")
            return redirect('listar-planos-economia')
    else:
        # Pré-preenchendo o campo "estabelecimento" no formulário
        form = PlanoEconomiaForm(initial={'estabelecimento': estabelecimento})

    return render(request, "criar_plano_economia.html", {"form": form, "estabelecimento": estabelecimento})


@login_required
def listar_planos(request):
    # Filtra os planos do usuário atual e ordena por 'posicao'
    planos = models.PlanoEconomia.objects.filter(
        user=request.user).order_by('posicao')

    # Renderiza a página com os planos ordenados
    return render(request, "listar_planos_economia.html", {"planos": planos})


@login_required
def exibir_plano_grafico(request, plano_id):
    plano = get_object_or_404(models.PlanoEconomia,
                              id=plano_id, user=request.user)

    categorias = [
        "Meta Gasto em R$ Mensal",
        "Meta kWh Mensal",
        "Consumo kWh Atual",
        "Custo R$ Atual",
        "Diferença kWh",
        "Diferença Custo",
    ]
    valores = [
        float(plano.meta_gasto_mensal),
        float(plano.meta_consumo_mensal),
        float(plano.consumo_atual),
        float(plano.custo_atual),
        float(plano.diferenca_kwh),
        float(plano.diferenca_custo),
    ]

    dados_grafico = {
        "categorias": categorias,
        "valores": valores,
    }

    return render(
        request,
        "exibir_plano_grafico.html",
        {"dados_grafico": dados_grafico, "plano": plano},
    )


@login_required
def editar_plano(request, id):
    plano = get_object_or_404(models.PlanoEconomia, id=id)

    if request.method == 'POST':
        form = PlanoEconomiaForm(request.POST, instance=plano)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plano atualizado com sucesso!')
            # Substitua pelo nome da URL que lista os planos
            return redirect('ver-plano-grafico', plano_id=plano.id)
        else:
            messages.error(
                request, 'Erro ao atualizar o plano. Verifique os dados fornecidos.')
    else:
        form = PlanoEconomiaForm(instance=plano)

    return render(request, 'editar_plano.html', {'form': form, 'plano': plano})


@login_required
def excluir_plano(request, id):
    plano = get_object_or_404(models.PlanoEconomia, id=id)

    if request.method == 'POST':
        plano.delete()
        messages.success(request, 'Plano excluído com sucesso!')
        # Substitua pelo nome da URL que lista os planos
        return redirect('listar-planos-economia')

    return render(request, 'confirmar_exclusao_plano.html', {'plano': plano})


@csrf_exempt
def salvar_ordem(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ordem = data.get('ordem', [])

            # Log os dados recebidos
            print(f"Dados recebidos: {ordem}")

            for item in ordem:
                plano_id = item.get('id')
                posicao = item.get('posicao')

                if plano_id is not None and posicao is not None:
                    updated_count = models.PlanoEconomia.objects.filter(
                        id=plano_id).update(posicao=posicao)
                    if updated_count == 0:
                        print(f"Plano com ID {plano_id} não encontrado.")

            return JsonResponse({'message': 'Ordem salva com sucesso!'}, status=200)

        except Exception as e:
            print(f"Erro ao salvar ordem: {e}")
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método não permitido'}, status=405)


@login_required
def dicas_economia(request, estabelecimento_id):
    # Obtenha o estabelecimento (considerando que o usuário só pode acessar seu próprio estabelecimento)
    estabelecimento = get_object_or_404(
        models.Estabelecimento, id=estabelecimento_id, user=request.user)

    # Criação de um objeto de DicasEconomia para esse estabelecimento
    dicas = DicasEconomia(estabelecimento)

    # Se o formulário de ajustes foi enviado, aplicamos os ajustes
    if request.method == 'POST':
        ajustes = dicas.aplicar_ajustes()

        # Adiciona uma mensagem de sucesso
        messages.success(request, 'Ajustes aplicados com sucesso!')

        # Redireciona para a página de listagem de planos de economia
        return redirect('listar-planos-economia')  # Substitua pela URL correta

    # Caso contrário, apenas exibe as dicas sem aplicar ajustes
    ajustes = models.Ajuste.objects.filter(
        estabelecimento=estabelecimento).order_by('-data_aplicacao')

    return render(request, 'dicas_economia.html', {
        'estabelecimento': estabelecimento,
        'dicas': dicas.calcular_dicas(),
        'ajustes': ajustes,  # Passa os ajustes aplicados para o template
    })
