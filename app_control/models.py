from django.utils import timezone
from django.db import models
from user_control.models import CustomUser, Setor
from user_control.views import add_user_activity


class Descricao_relatorio(models.Model):
    created_by = models.ForeignKey(
        CustomUser, null=True, related_name="description", on_delete=models.SET_NULL)
    description = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_description = self.description

    def save(self, *args, **kwargs):
        action = f"Adicionado nova descrição de relatório - '{self.description}'"
        if self.pk is not None:
            action = f"Atualizado nova descrição de relatório - '{self.old_description}' para '{self.description}'"
        super().save(*args, **kwargs)
        add_user_activity(self.created_by, action=action)

    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"Deletado descrição de relatório - '{self.description}'"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return self.description


class Rotina(models.Model):

    SITUACOES = (
        ('Diário', 'Diário'),
        ('Segunda-Feira', 'Segunda-Feira'),
        ('Terça-feira', 'Terça-feira'),
        ('Quarta-Feira', 'Quarta-Feira'),
        ('Quinta-Feira', 'Quinta-Feira'),
        ('Sexta-Feira', 'Sexta-Feira'),
        ('5° Dia Util', '5° Dia Util'),
        ('15 Dias', '15 Dias'),
        ('Mensal', 'Mensal'),
    )
    STATUS_CHOICES = (
        ('PENDENTE', 'Pendente'),
        ('REALIZADO', 'Realizado'),
        ('PREVISAO_EXECUCAO', 'Previsão de Execução'),
        ('REALIZADO_FORA_PRAZO', 'Realizado Fora do Prazo'),
    )

    created_by = models.ForeignKey(
        CustomUser, null=True, related_name="inventory_groups", on_delete=models.SET_NULL)
    descricao_relatorio = models.ForeignKey(
        Descricao_relatorio, on_delete=models.CASCADE, related_name='rotinas')
    prazo = models.CharField(
        max_length=15, choices=SITUACOES, default='Diário')
    data_mensal = models.DateField(null=True, blank=True)
    setor = models.ForeignKey(
        Setor, on_delete=models.CASCADE, related_name='setor')
    responsavel = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='responsavel')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.responsavel:
            if self.prazo != 'Mensal':
                self.data_mensal = None
            self.setor = self.responsavel.setor
        super(Rotina, self).save(*args, **kwargs)


class StatusDiarioRotina(models.Model):
    rotina = models.ForeignKey(
        Rotina, on_delete=models.CASCADE, related_name='status_diarios')
    data = models.DateField(default=timezone.now)
    status = models.CharField(
        max_length=20, choices=Rotina.STATUS_CHOICES, default='PENDENTE')
    usuario = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.rotina.descricao_relatorio} - {self.data} - {self.status} por {self.rotina.responsavel}"
