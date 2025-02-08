from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    # Associe o perfil ao usuário
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=255, default="Sem nome")
    # Permitindo que a data seja em branco ou nula
    data_nascimento = models.DateField(null=True, blank=True)
    # Permitindo endereço em branco
    endereco = models.CharField(max_length=255, blank=True, null=True)


def __str__(self):
    return f"Perfil de {self.user.username}"
