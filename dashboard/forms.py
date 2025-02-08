from django import forms
from .models import Equipamento

class EquipamentoForm(forms.Form):
    equipamentos = forms.ModelMultipleChoiceField(
        queryset=Equipamento.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Selecione os equipamentos que você possui:"
    )