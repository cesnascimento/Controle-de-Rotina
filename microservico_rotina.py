import os
import django
from django.utils import timezone
from app_control.models import Rotina, StatusDiarioRotina
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

def quinto_dia_util(ano, mes):
    contador_dias_uteis = 0
    dia = 1

    while contador_dias_uteis < 5:
        data_atual = datetime.date(ano, mes, dia)
        if data_atual.weekday() < 5:
            contador_dias_uteis += 1
        dia += 1

    return datetime.date(ano, mes, dia - 1)

def atualizar_criar_registro(prazo, hoje):
    rotinas = Rotina.objects.filter(prazo=prazo)  
    for rotina in rotinas: 
        rotina.status = 'PENDENTE'
        rotina.save()

        nova_rotina_status = StatusDiarioRotina(
            rotina=rotina,
            data=hoje,
            status='PENDENTE',
        )
        nova_rotina_status.save()
        print(f"Novo registro criado para a rotina {rotina.id} com status 'Pendente' e data atual")

def prazo_registros():
    hoje = timezone.now().date()
    dia_da_semana = hoje.weekday()

    if dia_da_semana in [5, 6]:
        print("Hoje é sábado ou domingo. Nenhuma operação será realizada.")
        return

    quinto_dia_util_atual = quinto_dia_util(hoje.year, hoje.month)
    prazos_semana = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira']

    prazos_a_atualizar = ['Diário']
    if dia_da_semana < 5:
        prazos_a_atualizar.append(prazos_semana[dia_da_semana])
    if hoje == quinto_dia_util_atual:
        prazos_a_atualizar.append('5° Dia Util')

    for prazo in prazos_a_atualizar:
        atualizar_criar_registro(prazo, hoje)

if __name__ == "__main__":
    prazo_registros()
