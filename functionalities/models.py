from django.db import models
from django.contrib.auth.models import User
from . import choice
from decimal import Decimal


class Estabelecimento(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    estabelecimento = models.CharField(max_length=255)
    created = models.DateField(auto_now_add=True)

    def total_equipamentos(self):
        return self.equipamentos.count()
    
    def total_gasto_equipamentos(self):
        return sum(equipamento.custoMensal for equipamento in self.equipamentos.all())
 

    def __str__(self):
        return f'{self.estabelecimento}'


class Equipamento(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    estabelecimento = models.ForeignKey(
        Estabelecimento, on_delete=models.CASCADE, related_name="equipamentos"
    )
    nome_personalizado = models.CharField(max_length=200)
    tipo = models.CharField(max_length=50, choices=choice.TIPOS_EQUIPAMENTO)
    potencia = models.PositiveIntegerField()  # Em watts
    horas_por_dia = models.PositiveIntegerField()  # 0 a 24 horas
    tarifa_por_kwh = models.DecimalField(
        max_digits=5, decimal_places=2)  # Custo por kWh em reais
    consumoMensalKwh = models.DecimalField(max_digits=5, decimal_places=2)
    custoMensal = models.DecimalField(
        max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Calcular consumo mensal em kWh
        self.consumoMensalKwh = (
            self.potencia * self.horas_por_dia * 30) / 1000

        # Calcular custo mensal em reais
        self.custoMensal = Decimal(self.consumoMensalKwh) * Decimal(str(self.tarifa_por_kwh))

        # Salvar normalmente
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_personalizado} ({self.tipo})"


class PlanoEconomia(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    estabelecimento = models.OneToOneField(
        Estabelecimento, on_delete=models.CASCADE, related_name="planos_economia"
    )
    meta_gasto_mensal = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Meta de gasto mensal em reais"
    )
    meta_consumo_mensal = models.DecimalField(
        max_digits=10, decimal_places=2,
        help_text="Meta de consumo mensal em kWh (opcional)"
    )
    created = models.DateField(auto_now_add=True)
    posicao = models.PositiveIntegerField(default=0)

    @property
    def consumo_atual(self):
        # Soma o consumo mensal de todos os equipamentos do estabelecimento
        return sum(equipamento.consumoMensalKwh for equipamento in self.estabelecimento.equipamentos.all())

    @property
    def custo_atual(self):
        # Soma o custo mensal de todos os equipamentos do estabelecimento
        return sum(equipamento.custoMensal for equipamento in self.estabelecimento.equipamentos.all())

    @property
    def diferenca_kwh(self):
        # Calcula a diferença entre a meta de consumo e o consumo atual
        if self.meta_consumo_mensal:
            return self.meta_consumo_mensal - self.consumo_atual
        return None

    @property
    def diferenca_custo(self):
        # Calcula a diferença entre a meta de gasto e o custo atual
        return self.meta_gasto_mensal - self.custo_atual

    def __str__(self):
        return f"Plano para {self.estabelecimento.estabelecimento} - Meta: {self.meta_gasto_mensal} R$"


from django.db import models

class Ajuste(models.Model):
    estabelecimento = models.ForeignKey('Estabelecimento', on_delete=models.CASCADE)
    equipamento = models.ForeignKey('Equipamento', on_delete=models.CASCADE)  # Campo obrigatório
    descricao = models.TextField()
    data_aplicacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ajuste para {self.estabelecimento.estabelecimento} - {self.data_aplicacao.strftime('%d/%m/%Y %H:%M')}"