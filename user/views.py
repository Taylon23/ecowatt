from django.contrib.auth.models import User
from django.utils.translation import activate as activate_ptbr
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignUpForm
from .forms import UserPerfilForm
from .models import UserPerfil, ConsumoMensal, Cupom
from dashboard import models as modelsDashboard
from django.contrib.auth.views import LoginView
import calendar
import locale
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deixar o usuário inativo até a confirmação
            user.save()

            # Gerar token e UID
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # Obter o domínio atual
            current_site = get_current_site(request)
            mail_subject = 'Confirme seu email'
            message = render_to_string(
                'activation_email.html',  # Template de e-mail de ativação
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token,
                }
            )

            # Enviar o e-mail
            send_mail(
                mail_subject,
                message,
                'noreply@yourdomain.com',  # Substitua pelo e-mail de envio
                [user.email],
                fail_silently=False,
                html_message=message,  # Definir o conteúdo do e-mail como HTML
            )

            # Adicionar mensagem de sucesso
            messages.success(
                request, 'Um link de ativação foi enviado para seu e-mail. Por favor, ative sua conta para fazer login.')

            return redirect('login')  # Redireciona para a página de login
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        # Decodificar o UID e obter o usuário
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')  # Redireciona para a página de login
    else:
        return HttpResponse("Link de ativação inválido!")

@login_required 
def alterar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantém o usuário logado após alterar a senha
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('perfil')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'alterar-senha.html', {'form': form})

@login_required
def deletar_conta(request):
    if request.method == 'POST':
        # Apaga o usuário autenticado
        user = request.user
        user.delete()
        messages.success(request, "Sua conta foi deletada com sucesso.")
        return redirect('dashboard')  # Ou qualquer página que você queira redirecionar após a exclusão
    
    return render(request, 'deletar-conta.html')



@login_required
def perfil(request):
    # Obtém o usuário logado
    user = request.user

    # Obtém o perfil estendido (UserPerfil) relacionado ao usuário
    try:
        perfil = user.perfil_energia  # Usa o related_name definido no modelo
    except UserPerfil.DoesNotExist:
        # Se o perfil não existir, cria um perfil vazio
        perfil = UserPerfil(usuario=user)
        perfil.save()

    return render(request, 'perfil.html', {'perfil': user, 'user_perfil': perfil})


@login_required
def completar_perfil(request):
    try:
        perfil = request.user.perfil_energia
    except UserPerfil.DoesNotExist:
        perfil = UserPerfil(usuario=request.user)

    if request.method == "POST":
        # Adicione request.FILES aqui
        form = UserPerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Redirecionar para a página de perfil
    else:
        form = UserPerfilForm(instance=perfil)

    return render(request, 'completar_perfil.html', {'form': form})


class CustomLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        # Se o usuário está sendo redirecionado devido a uma tentativa de acesso sem login
        if not request.user.is_authenticated and 'next' in request.GET:
            messages.error(
                request, 'Você precisa estar logado para acessar esta página.')
        return super().get(request, *args, **kwargs)
    
@login_required
def tarefas_concluidas(request):
    # Filtra as tarefas concluídas pelo usuário logado
    tarefas = modelsDashboard.UserTarefa.objects.filter(user=request.user, completo=True)
    return render(request, 'tarefas_concluidas.html', {'tarefas': tarefas})

@login_required
def historico_consumo(request):
    # Filtra o consumo mensal do usuário logado
    consumos = ConsumoMensal.objects.filter(usuario=request.user).order_by('-ano', '-mes')
    return render(request, 'historico-consumo.html', {'consumos': consumos})

@login_required
def meus_equipamentos(request):
    # Filtra os equipamentos do usuário logado
    equipamentos = modelsDashboard.UserEquipamento.objects.filter(user=request.user)
    return render(request, 'meus-equipamentos.html', {'equipamentos': equipamentos})


@login_required
def pagina_economia(request):
    try:
        perfil = request.user.perfil_energia
        if not perfil.cpf:
            messages.warning(
                request, "Você precisa completar seu perfil e cadastrar seu CPF para acessar a página de economia.")
            return redirect('completar-perfil')
    except UserPerfil.DoesNotExist:
        messages.warning(
            request, "Você precisa completar seu perfil e cadastrar seu CPF para acessar a página de economia.")
        return redirect('completar-perfil')

    # Configura o locale para português (Brasil)
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

    # Obtém o consumo atual
    consumo_atual = ConsumoMensal.objects.filter(usuario=request.user).last()
    consumo_anterior = None  # Inicializa a variável

    if consumo_atual:
        consumo_anterior = ConsumoMensal.objects.filter(
            usuario=request.user,
            ano__lte=consumo_atual.ano,
            mes__lt=consumo_atual.mes
        ).order_by('-ano', '-mes').first()

        if not consumo_anterior and consumo_atual.mes == 1:
            consumo_anterior = ConsumoMensal.objects.filter(
                usuario=request.user,
                ano=consumo_atual.ano - 1,
                mes=12
            ).order_by('-ano', '-mes').first()

        economia = consumo_atual.calculo_economia()
        economia_formatada = f"{abs(economia):.1f}" if economia is not None else "0.0"

        historico_consumos = ConsumoMensal.objects.filter(
            usuario=request.user).order_by('-ano', '-mes')

        for consumo in historico_consumos:
            consumo.variacao = consumo.calcular_variacao()

        mes_atual_nome = calendar.month_name[consumo_atual.mes]
        mes_anterior_nome = calendar.month_name[consumo_anterior.mes] if consumo_anterior else "Mês Desconhecido"
        cupom = Cupom.objects.filter(usuario=request.user).last()
        mensagem_cupom = f"{cupom.codigo}" if cupom else "Continue economizando para ganhar um cupom!"
    else:
        economia = economia_formatada = None
        historico_consumos = []
        mes_atual_nome = mes_anterior_nome = "Mês Desconhecido"
        mensagem_cupom = "Nenhum consumo registrado ainda."

    return render(request, 'pagina_economia.html', {
        'consumo_atual': consumo_atual,
        'consumo_anterior': consumo_anterior,
        'mensagem_cupom': mensagem_cupom,
        'historico_consumos': historico_consumos,
        'economia': economia,
        'economia_formatada': economia_formatada,
        'mes_atual_nome': mes_atual_nome,
        'mes_anterior_nome': mes_anterior_nome,
    })
