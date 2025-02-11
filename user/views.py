from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignUpForm
from .forms import UserPerfilForm
from .models import UserPerfil, ConsumoMensal
from django.contrib.auth.views import LoginView
from datetime import date
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


def gerar_cupom(user):
    perfil = user.perfil_energia
    if perfil.cupom:  # Verifica se já existe um cupom
        return perfil.cupom  # Retorna o cupom existente

    # Gera um novo cupom apenas se não houver um já existente
    import uuid
    cupom = str(uuid.uuid4()).split('-')[0].upper()
    perfil.cupom = cupom
    perfil.save()
    return cupom


@login_required
def pagina_economia(request):
    try:
        perfil = request.user.perfil_energia
    except UserPerfil.DoesNotExist:
        messages.error(
            request, "Perfil de energia não cadastrado. Complete seu cadastro.")
        return redirect('cadastro_perfil')

    mes_atual = date.today().month
    ano_atual = date.today().year

    # Salva ou atualiza o consumo atual
    consumo_atual_obj, created = ConsumoMensal.objects.get_or_create(
        perfil=perfil,
        mes=mes_atual,
        ano=ano_atual,
        defaults={'consumo': perfil.consumo_atual}
    )

    if not created:  # Atualiza se já existir
        consumo_atual_obj.consumo = perfil.consumo_atual
        consumo_atual_obj.save()

    # Busca o consumo do mês anterior
    mes_anterior = mes_atual - 1 if mes_atual > 1 else 12
    ano_anterior = ano_atual if mes_atual > 1 else ano_atual - 1

    try:
        consumo_anterior_obj = ConsumoMensal.objects.get(
            perfil=perfil, mes=mes_anterior, ano=ano_anterior)
        consumo_anterior = consumo_anterior_obj.consumo
    except ConsumoMensal.DoesNotExist:
        consumo_anterior = 0  # Se não houver registro do mês anterior

    economia = consumo_anterior - perfil.consumo_atual

    # Verificação para gerar cupom
    if mes_atual != perfil.ultimo_consumo_registrado:
        if economia > 50:
            cupom = gerar_cupom(request.user)
            perfil.cupom = cupom  # Salva o cupom no perfil do usuário
            mensagem_cupom = f"Parabéns! Você ganhou um cupom de desconto: {cupom}"
        else:
            mensagem_cupom = "Continue economizando para ganhar um cupom!"

        perfil.ultimo_consumo_registrado = mes_atual
        perfil.save()
    else:
        mensagem_cupom = f"Seu cupom: {perfil.cupom}" if perfil.cupom else "Continue economizando para ganhar um cupom!"

    # Histórico de consumos
    historico_consumos = ConsumoMensal.objects.filter(
        perfil=perfil).order_by('-ano', '-mes')

    return render(request, 'pagina_economia.html', {
        'economia': economia,
        'mes_atual': consumo_atual_obj.consumo,
        'mes_anterior': consumo_anterior,
        'mensagem_cupom': mensagem_cupom,
        'historico_consumos': historico_consumos,
    })
