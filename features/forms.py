from django import forms
from . import choice
from . import models


class CalculoConsumoForm(forms.ModelForm):

    class Meta:
        model = models.Equipamento
        fields = ['estabelecimento','nome_personalizado', 'tipo',
                  'potencia', 'horas_por_dia', 'tarifa_por_kwh']
        labels = {
            'estabelecimento': 'Meu estabelecimento',
            'nome_personalizado': 'Nome do Equipamento',
            'tipo': 'Tipo de Equipamento',
            'potencia': 'Potência (W)',
            'horas_por_dia': 'Horas de Uso por Dia',
            'tarifa_por_kwh': 'Tarifa por kWh (R$)',
        }
        widgets = {
            'tipo': forms.Select(choices=choice.TIPOS_EQUIPAMENTO),
            'nome_personalizado': forms.TextInput(attrs={'placeholder': 'Meu eletrônico'}),
            'potencia': forms.NumberInput(attrs={'placeholder': 'Exemplo: 500'}),
            'horas_por_dia': forms.NumberInput(attrs={'placeholder': 'Exemplo: 5'}),
            'tarifa_por_kwh': forms.NumberInput(attrs={'placeholder': 'Exemplo: 0.75'}),
            'estabelecimento': forms.Select(),
        }

    # Aqui você pode adicionar validações extras, se necessário:
    def clean_potencia(self):
        potencia = self.cleaned_data.get('potencia')
        if potencia <= 0:
            raise forms.ValidationError("A potência deve ser maior que zero.")
        return potencia

    def clean_horas_por_dia(self):
        horas = self.cleaned_data.get('horas_por_dia')
        if horas < 0 or horas > 24:
            raise forms.ValidationError(
                "O valor de horas por dia deve estar entre 0 e 24.")
        return horas

    def clean_tarifa_por_kwh(self):
        tarifa = self.cleaned_data.get('tarifa_por_kwh')
        if tarifa <= 0:
            raise forms.ValidationError(
                "A tarifa por kWh deve ser maior que zero.")
        return tarifa


class EstabelecimentoForm(forms.ModelForm):
    class Meta:
        model = models.Estabelecimento
        fields = ['estabelecimento']
        label = {'estabelecimento': 'Meu estabelecimento'}
        widgets = {'estabelecimento': forms.TextInput(attrs={'placeholder': 'Exemplo: Minha casa'})}
