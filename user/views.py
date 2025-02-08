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
from .models import UserPerfil
from django.contrib.auth.views import LoginView
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
        form = UserPerfilForm(request.POST, request.FILES, instance=perfil)  # Adicione request.FILES aqui
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
