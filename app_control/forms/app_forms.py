from django import forms
from ..models import Rotina, Descricao_relatorio

class DescricaoRelatorioForm(forms.ModelForm):
    class Meta:
        model = Descricao_relatorio
        fields = ['description']
        labels = {'description': 'Descrição de Relatório'}


class EditarDescricaoRelatorioForm(forms.ModelForm):
    class Meta:
        model = Descricao_relatorio
        fields = ['description']
        labels = {'description': 'Descrição de Relatório'}


class RotinaForm(forms.ModelForm):
    class Meta:
        model = Rotina
        fields = ['descricao_relatorio', 'setor', 'responsavel', 'situacao']
        labels = {
            'descricao_relatorio': 'Descrição de Relatório',
            'responsavel': 'Responsável',
            'situacao': 'Situação',
        }

