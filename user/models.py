from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Associe o perfil ao usuário
    nome_completo = models.CharField(max_length=255, default="Sem nome")
    data_nascimento = models.DateField(null=True, blank=True)  # Permitindo que a data seja em branco ou nula
    endereco = models.CharField(max_length=255, blank=True, null=True)  # Permitindo endereço em branco

    def __str__(self):
        return f"Perfil de {self.user.username}"

