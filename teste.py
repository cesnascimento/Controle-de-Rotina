import os
import django
from django.utils import timezone
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from app_control.models import Rotina, StatusDiarioRotina

def adicionar_status_realizado(email_responsavel, prazo, datas):
    rotinas = Rotina.objects.filter(responsavel=3, prazo=prazo)

    for rotina in rotinas:
        for data in datas:
            nova_rotina_status = StatusDiarioRotina(
                rotina=rotina,
                data=data,
                status='REALIZADO'
            )
            nova_rotina_status.save()
            print(
                f"Registro REALIZADO criado para a rotina {rotina.id} na data {data}")


if __name__ == "__main__":
    email_responsavel = "lcanto@dermage.com.br"
    prazo = "Diário"
    # Ajuste o ano conforme necessário
    datas = [datetime.date(2023, 12, dia) for dia in [1, 4, 5, 6, 7, 8, 11]]

    adicionar_status_realizado(email_responsavel, prazo, datas)
