from django.shortcuts import render, redirect, get_object_or_404
from .forms import CalculoConsumoForm, EstabelecimentoForm
from . import models
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
            return redirect('lista-equipamentos', estabelecimento_id=equipamento.estabelecimento.id)
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
