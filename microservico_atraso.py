import os
import django
import datetime
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from app_control.models import Rotina, StatusDiarioRotina

def quinto_dia_util(ano, mes):
    contador_dias_uteis = 0
    dia = 1
    while contador_dias_uteis < 5:
        data_atual = datetime.date(ano, mes, dia)
        if data_atual.weekday() < 5:  # Dias da semana (0-4 são segunda a sexta)
            contador_dias_uteis += 1
        dia += 1
    return datetime.date(ano, mes, dia - 1)

def atualizar_status_rotinas(prazo, data):
    rotinas = Rotina.objects.filter(prazo=prazo)
    for rotina in rotinas:
        status_diario = StatusDiarioRotina.objects.filter(rotina=rotina, data=data, status='PREVISAO_EXECUCAO').first()
        if status_diario:
            status_diario.status = 'PENDENTE'
            status_diario.save()
            rotina.status = 'PENDENTE'
            rotina.save()
            print(f"Status da rotina {prazo} {rotina.id} atualizado para 'Pendente' na data {data}")

def atualizar_status_dia_anterior():
    hoje = timezone.now().date()
    ontem = hoje - datetime.timedelta(days=1)

    # Atualiza as rotinas diárias do dia anterior para 'PENDENTE' se necessário
    atualizar_status_rotinas('Diário', ontem)

    # Atualiza rotinas semanais e do '5° Dia Útil' da semana anterior se necessário
    dia_semana_anterior = hoje - datetime.timedelta(days=7)
    prazos_semana = ['Segunda-Feira', 'Terça-Feira', 'Quarta-Feira', 'Quinta-Feira', 'Sexta-Feira']
    prazo_semana_anterior = prazos_semana[dia_semana_anterior.weekday()]
    atualizar_status_rotinas(prazo_semana_anterior, dia_semana_anterior)

    mes_anterior = (hoje.replace(day=1) - datetime.timedelta(days=1)).month
    ano_mes_anterior = hoje.year if mes_anterior != 12 else hoje.year - 1
    quinto_dia_util_mes_anterior = quinto_dia_util(ano_mes_anterior, mes_anterior)
    atualizar_status_rotinas('5° Dia Util', quinto_dia_util_mes_anterior)

def prazo_registros():
    atualizar_status_dia_anterior()

if __name__ == "__main__":
    prazo_registros()
