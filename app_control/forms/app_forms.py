from django import forms
from user_control.models import CustomUser
from ..models import Rotina, Descricao_relatorio, StatusDiarioRotina
from django.forms import ModelChoiceField
from django.utils import timezone


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


class CustomUserChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.fullname


class RotinaForm(forms.ModelForm):
    responsavel = CustomUserChoiceField(queryset=CustomUser.objects.all())

    class Meta:
        model = Rotina
        fields = ['descricao_relatorio', 'prazo', 'responsavel']
        labels = {
            'descricao_relatorio': 'Descrição de Relatório',
            'responsavel': 'Responsável',
        }


class AtualizarStatusRotinaForm(forms.ModelForm):

    STATUS_CHOICES = (
        ('REALIZADO', 'Realizado'),
        ('INVENTARIO_GERAL', 'Inventário Geral'),
        ('JUSTIFICADO', 'Justificado'),
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = StatusDiarioRotina
        fields = ['status', 'data']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            # Não defina 'initial' aqui
        }
