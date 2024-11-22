from django.db import models
from django.contrib.auth.models import User
from . import choice


class Equipamento(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    nome_personalizado = models.CharField(max_length=200)
    tipo = models.CharField(max_length=50, choices=choice.TIPOS_EQUIPAMENTO)
    potencia = models.PositiveIntegerField()  # Em watts
    horas_por_dia = models.PositiveIntegerField()  # 0 a 24 horas
    tarifa_por_kwh = models.DecimalField(
        max_digits=5, decimal_places=2)  # Custo por kWh em reais
    consumoMensalKwh = models.DecimalField(max_digits=5, decimal_places=2)
    custoMensal = models.DecimalField(
        max_digits=10, decimal_places=2)  # Corrigido aqui

    def save(self, *args, **kwargs):
        # Calcular consumo mensal em kWh
        self.consumoMensalKwh = (
            self.potencia * self.horas_por_dia * 30) / 1000

        # Calcular custo mensal em reais
        self.custoMensal = self.consumoMensalKwh * float(self.tarifa_por_kwh)

        # Salvar normalmente
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_personalizado} ({self.tipo})"
