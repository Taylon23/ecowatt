from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")

        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if User.objects.filter(username=username).exists():
            self.add_error('username', 'Este nome de usuário já está em uso. Por favor, escolha outro.')

        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Este e-mail já está em uso.')

        return cleaned_data
