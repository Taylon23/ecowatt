from django.db import models
from django.contrib.auth.models import User
from datetime import date
import random
import string


class Cupom(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=20, unique=True)
    data_geracao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cupom de {self.usuario.username} - {self.codigo}"

    @staticmethod
    def gerar_cupom(usuario):
        while True:
            # Gera um código aleatório
            codigo = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=10))

            # Verifica se o código já existe
            if not Cupom.objects.filter(codigo=codigo).exists():
                # Cria o cupom com o código único
                cupom = Cupom.objects.create(usuario=usuario, codigo=codigo)
                return cupom.codigo  # Retorna o código gerado


class UserPerfil(models.Model):
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='perfil_energia')
    nome_completo = models.CharField(max_length=220)
    foto = models.ImageField(upload_to='perfil_fotos/', blank=True,
                             null=True, help_text="Foto de perfil do usuário")
    cpf = models.CharField(max_length=14, help_text="CPF do usuário")
    data_nascimento = models.DateField(
        help_text="Data de nascimento do usuário", default=date(2007, 1, 1))
    cep = models.CharField(max_length=9, help_text="CEP do usuário")
    endereco = models.CharField(
        max_length=220, blank=True, null=True, help_text="Endereço completo")
    estado = models.CharField(
        max_length=2, blank=True, null=True, help_text="Estado da instalação (ex: PI)")
    cidade = models.CharField(
        max_length=100, blank=True, null=True, help_text="Cidade do usuário")
    token = models.CharField(max_length=255, blank=True,
                             null=True, help_text="Token de autenticação")

    def __str__(self):
        return f"Perfil de Energia de {self.usuario.username}"


class ConsumoMensal(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    consumo_atual = models.FloatField(
        default=0, help_text="Consumo atual em kWh")
    mes = models.IntegerField(help_text="Mês do consumo (1-12)")
    ano = models.IntegerField(help_text="Ano do consumo")

    def calcular_variacao(self):
        # Obtém o mês e o ano anteriores
        mes_anterior = self.mes - 1
        ano_anterior = self.ano

        if mes_anterior == 0:
            mes_anterior = 12
            ano_anterior -= 1

        consumo_anterior = ConsumoMensal.objects.filter(
            usuario=self.usuario,
            mes=mes_anterior,
            ano=ano_anterior
        ).first()

        print(
            f"Consumo atual: {self.consumo_atual}, Consumo anterior: {consumo_anterior.consumo_atual if consumo_anterior else 'não encontrado'}")

        if consumo_anterior and consumo_anterior.consumo_atual != 0:
            variacao = ((self.consumo_atual - consumo_anterior.consumo_atual) /
                        consumo_anterior.consumo_atual) * 100
            print(f"Variação calculada: {variacao}%")
            return round(variacao, 1)  # Arredonda para 1 casa decimal
        return None

    def save(self, *args, **kwargs):
        # Verifica o consumo do mês anterior
        mes_anterior = self.mes - 1
        ano_anterior = self.ano

        if mes_anterior == 0:
            mes_anterior = 12
            ano_anterior -= 1

        # Verifica se já existe um consumo anterior para comparar
        consumo_anterior = ConsumoMensal.objects.filter(
            usuario=self.usuario,
            mes=mes_anterior,
            ano=ano_anterior
        ).first()

        if consumo_anterior:
            economia = consumo_anterior.consumo_atual - self.consumo_atual
            if economia >= 50:
                # Gera um novo cupom toda vez que a economia for >= 50 kWh
                Cupom.gerar_cupom(self.usuario)

        super().save(*args, **kwargs)

    def calculo_economia(self):
        mes_anterior = self.mes - 1
        ano_anterior = self.ano

        if mes_anterior == 0:
            mes_anterior = 12
            ano_anterior -= 1

        consumo_anterior = ConsumoMensal.objects.filter(
            usuario=self.usuario,
            mes=mes_anterior,
            ano=ano_anterior
        ).first()

        if consumo_anterior:
            return consumo_anterior.consumo_atual - self.consumo_atual
        return None  # Retorna None se não houver consumo anterior

    def __str__(self):
        return f"Consumo de {self.usuario.username} em {self.mes}/{self.ano}"

    class Meta:
        unique_together = ('usuario', 'mes', 'ano')
