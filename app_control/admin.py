from django.contrib import admin
from .models import Descricao_relatorio, Rotina, StatusDiarioRotina

admin.site.register((Descricao_relatorio, Rotina, StatusDiarioRotina))
