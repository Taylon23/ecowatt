from django.shortcuts import render, redirect
from .forms import CalculoConsumoForm
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def calculo_consumo(request):
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
            return redirect('listar-equipamentos')
    else:
        form = CalculoConsumoForm()

    return render(request, 'calculo_consumo.html', {'form': form})


@login_required
def listar_equipamentos(request):
    # Verifique se o usuário está logado
    print(f"Usuário logado: {request.user}")
    
    # Busca os equipamentos do usuário logado
    equipamentos = models.Equipamento.objects.filter(user=request.user)
    
    # Verifique se há equipamentos para o usuário
    print(f"Equipamentos encontrados: {equipamentos.count()}")
    
    context = {
        'equipamentos': equipamentos
    }

    return render(request, 'listar_equipamentos.html', context)