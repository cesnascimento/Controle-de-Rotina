from django.db import models
from user_control.models import CustomUser
from user_control.views import add_user_activity


class Descricao_relatorio(models.Model):
  #created_by = models.ForeignKey(CustomUser, null=True, related_name="description", on_delete=models.SET_NULL)
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
    #add_user_activity(self.created_by, action=action)

  def delete(self, *args, **kwargs):
    created_by = self.created_by
    action = f"Deletado descrição de relatório - '{self.description}'"
    super().delete(*args, **kwargs)
    add_user_activity(created_by, action=action)

  def __str__(self):
    return self.description

class Setor(models.Model):
  created_by = models.ForeignKey(CustomUser, null=True, related_name="user_sector", on_delete=models.SET_NULL)
  sector = models.CharField(max_length=500, unique=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ['id']

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.old_sector = self.sector
  
  def save(self, *args, **kwargs):
    action = f"Adicionado novo setor - '{self.sector}'"
    if self.pk is not None:
        action = f"Atualizado novo setor - '{self.old_sector}' para '{self.sector}'"
    super().save(*args, **kwargs)
    add_user_activity(self.created_by, action=action)

  def delete(self, *args, **kwargs):
    created_by = self.created_by
    action = f"Deletado setor - '{self.sector}'"
    super().delete(*args, **kwargs)
    add_user_activity(created_by, action=action)

  def __str__(self):
    return self.sector

class Responsavel(models.Model):
  created_by = models.ForeignKey(CustomUser, null=True, related_name="responavel", on_delete=models.SET_NULL)
  name = models.CharField(max_length=500, unique=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ['id']

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.old_name = self.name
  
  def save(self, *args, **kwargs):
    action = f"Adicionado novo setor - '{self.name}'"
    if self.pk is not None:
        action = f"Atualizado novo setor - '{self.old_name}' para '{self.name}'"
    super().save(*args, **kwargs)
    add_user_activity(self.created_by, action=action)

  def delete(self, *args, **kwargs):
    created_by = self.created_by
    action = f"Deletado setor - '{self.name}'"
    super().delete(*args, **kwargs)
    add_user_activity(created_by, action=action)

  def __str__(self):
    return self.name

class Rotina(models.Model):

  SITUACOES = (
    ('prevista', 'Prevista'),
    ('realizada', 'Realizada'),
    ('fora_do_prazo', 'Fora do Prazo'),
  )

  created_by = models.ForeignKey(CustomUser, null=True, related_name="inventory_groups", on_delete=models.SET_NULL)
  descricao_relatorio = models.ForeignKey(Descricao_relatorio, on_delete=models.CASCADE, related_name='rotinas')
  setor = models.ForeignKey(Setor, on_delete=models.CASCADE, related_name='setor')
  responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE, related_name='responsavel')
  situacao = models.CharField(max_length=15, choices=SITUACOES, default='prevista')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)