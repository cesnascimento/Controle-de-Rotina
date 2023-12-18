from django.shortcuts import get_object_or_404, render, redirect
from user_control.models import CustomUser
from .forms.app_forms import AtualizarStatusRotinaForm, RotinaForm, DescricaoRelatorioForm
from .models import Rotina, Descricao_relatorio, Setor, StatusDiarioRotina
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Rotina


@login_required
def add_rotina(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado. Você precisa ser administrador.")
    if request.method == 'POST':
        form = RotinaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_rotina')
    else:
        form = RotinaForm()

    return render(request, 'app/add_or_edit_rotina.html', {'form': form})


@login_required
def edit_rotina(request, id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado. Você precisa ser administrador.")
    rotina = Rotina.objects.get(id=id)
    if request.method == 'POST':
        form = RotinaForm(request.POST, instance=rotina)
        if form.is_valid():
            form.save()
            return redirect('listar_rotina')
    else:
        form = RotinaForm(instance=rotina)

    return render(request, 'app/add_or_edit_rotina.html', {'form': form})


@login_required
def delete_rotina(request, id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado. Você precisa ser administrador.")
    rotina = get_object_or_404(Rotina, id=id)
    rotina.delete()
    return redirect('listar_rotina')


@login_required
def listar_rotina(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado. Você precisa ser administrador.")
    rotinas = Rotina.objects.all()
    return render(request, 'app/list_rotina.html', {'rotinas': rotinas})


@login_required
def atualizar_status_rotina(request, pk):
    rotina = get_object_or_404(Rotina, pk=pk, responsavel=request.user)

    # Obter o último status para a data atual, se existir
    ultimo_status = StatusDiarioRotina.objects.filter(
        rotina=rotina).order_by('-id').first()

    if request.method == 'POST':
        form = AtualizarStatusRotinaForm(request.POST)
        if form.is_valid():
            novo_status = form.save(commit=False)
            novo_status.rotina = rotina
            novo_status.usuario = request.user

            data_realizacao = form.cleaned_data.get('data')
            if rotina.prazo == "Diário" and data_realizacao != timezone.now().date():
                novo_status.status = 'REALIZADO_FORA_PRAZO'
            else:
                novo_status.status = form.cleaned_data['status']

            novo_status.save()

            rotina.status = novo_status.status
            rotina.save()
            return redirect('minhas_rotinas')
    else:
        form = AtualizarStatusRotinaForm(initial={'data': timezone.now(
        ).date().strftime('%Y-%m-%d')}, instance=ultimo_status)

    return render(request, 'app/atualizar_status_rotina.html', {'form': form, 'rotina': rotina})


@login_required
def minhas_rotinas(request):
    data_atual = timezone.now().date()
    rotinas = Rotina.objects.filter(responsavel=request.user)
    status = StatusDiarioRotina.objects.filter(
        rotina__in=rotinas, data=data_atual)
    # Adicionar lógica para outras periodicidades se necessário
    return render(request, 'app/minhas_rotinas.html',
                  {
                      'rotinas': rotinas,
                      'status_diarios': status}
                  )


# Descrição de Relatorio

@login_required
def add_descricao_relatorio(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado. Você precisa ser administrador.")
    if request.method == 'POST':
        form_descricao_relatorio = DescricaoRelatorioForm(request.POST)
        form_descricao_relatorio.fields['description'].label = "Descrição de Relatório"
        if form_descricao_relatorio.is_valid():
            descricao_relatorio = form_descricao_relatorio.save(commit=False)
            descricao_relatorio.created_by = request.user
            descricao_relatorio.save()
            return redirect('list_descricao_relatorio')
    else:
        form_descricao_relatorio = DescricaoRelatorioForm()
        form_descricao_relatorio.fields['description'].label = "Descrição de Relatório"

    return render(request, 'app/add_descricao_relatorio.html', {'form_descricao_relatorio': form_descricao_relatorio})


@login_required
def edit_descricao_relatorio(request, id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado. Você precisa ser administrador.")
    descricao_relatorio = Descricao_relatorio.objects.get(id=id)
    if request.method == 'POST':
        form_descricao_relatorio = DescricaoRelatorioForm(
            request.POST, instance=descricao_relatorio)
        if form_descricao_relatorio.is_valid():
            form_descricao_relatorio.save()
            return redirect('list_descricao_relatorio')
    else:
        form_descricao_relatorio = DescricaoRelatorioForm(
            instance=descricao_relatorio)

    return render(request, 'app/add_descricao_relatorio.html', {'form_descricao_relatorio': form_descricao_relatorio, 'descricao_relatorio': descricao_relatorio})


@login_required
def list_descricao_relatorio(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado. Você precisa ser administrador.")
    descricoes = Descricao_relatorio.objects.all()
    return render(request, 'app/list_descricao_relatorio.html', {'descricoes': descricoes})

def delete_descricao_relatorio(request, id):
    if not request.user.is_staff:
            return HttpResponseForbidden("Acesso negado. Você precisa ser administrador.")
    descricao = get_object_or_404(Descricao_relatorio, id=id)
    descricao.delete()
    return redirect('list_descricao_relatorio')


@login_required
def gerencia_rotina(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado. Você precisa ser administrador.")
    status_diarios = StatusDiarioRotina.objects.all()

    responsaveis = CustomUser.objects.all()
    setores = Setor.objects.all()
    descricoes = Descricao_relatorio.objects.all()
    prazos = Rotina.objects.values_list('prazo', flat=True).distinct()
    status_diarios = StatusDiarioRotina.objects.all()

    responsavel_query = request.GET.get('responsavel')
    setor_query = request.GET.get('setor')
    descricao_query = request.GET.get('descricao')
    prazo_query = request.GET.get('prazo')
    status_query = request.GET.get('status')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if responsavel_query:
        status_diarios = status_diarios.filter(usuario__id=responsavel_query)
    if setor_query:
        status_diarios = status_diarios.filter(rotina__setor__id=setor_query)
    if descricao_query:
        status_diarios = status_diarios.filter(
            rotina__descricao_relatorio__id=descricao_query)
    if prazo_query:
        status_diarios = status_diarios.filter(rotina__prazo=prazo_query)
    if status_query:
        status_diarios = status_diarios.filter(status=status_query)
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        status_diarios = status_diarios.filter(data__gte=start_date)
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        status_diarios = status_diarios.filter(data__lte=end_date)

    return render(request, 'app/gerencia_rotina.html', {
        'status_diarios': status_diarios,
        'responsaveis': responsaveis,
        'setores': setores,
        'descricoes': descricoes,
        'prazos': prazos,
        'status_choices': Rotina.STATUS_CHOICES,
    })

def quinto_dia_util(mes, ano):
    dia = 1
    dias_uteis = 0
    while dias_uteis < 5:
        data_atual = datetime(ano, mes, dia)
        # Segunda-feira = 0, Domingo = 6
        if data_atual.weekday() < 5:  # Segunda a sexta
            dias_uteis += 1
        if dias_uteis == 5:
            return data_atual
        dia += 1


def e_data_correspondente(rotina, dia):
    # Verifica se a data corresponde à data_mensal ou 15 dias após
    if rotina.prazo in ['Mensal', '15 Dias'] and rotina.data_mensal:
        if rotina.prazo == 'Mensal':
            print('aqui data correspondnte', rotina.data_mensal)
            return dia.date() == rotina.data_mensal
        elif rotina.prazo == '15 Dias':
            print('aqui data correspondnte', rotina.data_mensal)
            data_15_dias = rotina.data_mensal + timedelta(days=15)
            # Ajusta para o próximo mês se necessário
            if data_15_dias.month != rotina.data_mensal.month:
                data_15_dias = data_15_dias.replace(month=rotina.data_mensal.month + 1, day=1)
            return dia.date() == rotina.data_mensal or dia.date() == data_15_dias
    print('aqui data correspondnte', rotina.data_mensal)
    return False

def obter_status_para_data(rotina, dia):
    status = StatusDiarioRotina.objects.filter(
        rotina=rotina, data=dia).order_by('-data', '-id').first()

    if status:
        status_para_letra = {
            'PENDENTE': 'A',
            'REALIZADO': 'R',
            'PREVISAO_EXECUCAO': 'P',
            'REALIZADO_FORA_PRAZO': 'F',
            'INVENTARIO_GERAL': 'I',
            'JUSTIFICADO': 'J'
        }
        return status_para_letra.get(status.status, '')
    else:
        dias_da_semana = {
            0: 'Segunda-Feira',
            1: 'Terça-feira',
            2: 'Quarta-Feira',
            3: 'Quinta-Feira',
            4: 'Sexta-Feira',
        }
        dia_da_semana = dia.weekday()
        quinto_dia_util_do_mes = quinto_dia_util(dia.month, dia.year)

        # Verifica se a data corresponde à rotina diária, semanal ou no 5° dia útil do mês
        if (rotina.prazo == 'Diário' or 
            rotina.prazo == dias_da_semana.get(dia_da_semana) or
            (rotina.prazo == '5° Dia Util' and dia.date() == quinto_dia_util_do_mes.date())):
            return 'P'
        return ''
        



def get_dias_uteis(mes, ano):
    dias_do_mes = []
    data = datetime(ano, mes, 1)
    while data.month == mes:
        if data.weekday() < 5:  # 0-4 são dias de semana (segunda a sexta)
            dias_do_mes.append(data)
        data += timedelta(days=1)
    return dias_do_mes


@login_required
def calendario_rotina(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado. Você precisa ser administrador.")

    ano_atual, mes_atual = datetime.now().year, datetime.now().month
    dias_do_mes = get_dias_uteis(mes_atual, ano_atual)
    rotinas = Rotina.objects.select_related('responsavel').order_by(
        'responsavel__fullname', 'created_at')

    responsaveis = CustomUser.objects.all()
    setores = Setor.objects.all()
    descricoes = Descricao_relatorio.objects.all()
    prazos = Rotina.objects.values_list('prazo', flat=True).distinct()

    # Captura os valores dos filtros do pedido GET
    responsavel_query = request.GET.get('responsavel')
    setor_query = request.GET.get('setor')
    descricao_query = request.GET.get('descricao')
    prazo_query = request.GET.get('prazo')

    # Aplica os filtros
    if responsavel_query:
        rotinas = rotinas.filter(responsavel__id=responsavel_query)
    if setor_query:
        rotinas = rotinas.filter(setor__id=setor_query)
    if descricao_query:
        rotinas = rotinas.filter(descricao_relatorio__id=descricao_query)
    if prazo_query:
        rotinas = rotinas.filter(prazo=prazo_query)


    rotinas_com_status = []
    for rotina in rotinas:
        status_diarios = [obter_status_para_data(
            rotina, dia) for dia in dias_do_mes]
        rotinas_com_status.append({
            'rotina': rotina,
            'status_diarios': status_diarios
        })

    return render(request, 'app/seu_template_calendario.html', {
        'rotinas_com_status': rotinas_com_status,
        'dias_do_mes': dias_do_mes,
        'responsaveis': responsaveis,
        'setores': setores,
        'descricoes': descricoes,
        'prazos': prazos,
    })
