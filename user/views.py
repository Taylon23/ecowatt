from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignUpForm
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
                    'STATIC_URL': settings.STATIC_URL,  # Passa a URL estática no contexto
                }
            )

            # Enviar o e-mail
            send_mail(
                mail_subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
                html_message=message,  # Definir o conteúdo do e-mail como HTML
            )
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
