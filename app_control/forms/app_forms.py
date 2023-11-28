from django import forms
from ..models import Rotina, Descricao_relatorio, Setor, Responsavel


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


class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        fields = ['sector']
        labels = {'sector': 'Setor'}


class ResponsavelForm(forms.ModelForm):
    class Meta:
        model = Responsavel
        fields = ['name']
        labels = {'name': 'Nome'}


class RotinaForm(forms.ModelForm):
    class Meta:
        model = Rotina
        fields = ['descricao_relatorio', 'setor', 'responsavel', 'situacao']
        labels = {
            'descricao_relatorio': 'Descrição de Relatório',
            'responsavel': 'Responsável',
            'situacao': 'Situação',
        }
