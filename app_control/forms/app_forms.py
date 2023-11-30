from django import forms
from user_control.models import CustomUser
from ..models import Rotina, Descricao_relatorio, Setor, Responsavel, StatusDiarioRotina
from django.forms import ModelChoiceField, Select


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


class CustomUserChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.fullname


class RotinaForm(forms.ModelForm):
    responsavel = CustomUserChoiceField(queryset=CustomUser.objects.all())

    class Meta:
        model = Rotina
        fields = ['descricao_relatorio', 'prazo', 'setor', 'responsavel']
        labels = {
            'descricao_relatorio': 'Descrição de Relatório',
            'responsavel': 'Responsável',
        }


class AtualizarStatusRotinaForm(forms.ModelForm):
    class Meta:
        model = StatusDiarioRotina
        fields = ['status']
