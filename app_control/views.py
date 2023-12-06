from django.shortcuts import get_object_or_404, render, redirect
from user_control.models import CustomUser
from .forms.app_forms import AtualizarStatusRotinaForm, RotinaForm, DescricaoRelatorioForm
from .models import Rotina, Descricao_relatorio, Setor, StatusDiarioRotina
from django.utils import timezone
from datetime import datetime, timedelta
import calendar

# Rotina


def add_rotina(request):
    if request.method == 'POST':
        form = RotinaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_rotina')
    else:
        form = RotinaForm()

    return render(request, 'app/add_or_edit_rotina.html', {'form': form})


def edit_rotina(request, id):
    rotina = Rotina.objects.get(id=id)
    if request.method == 'POST':
        form = RotinaForm(request.POST, instance=rotina)
        if form.is_valid():
            form.save()
            return redirect('listar_rotina')
    else:
        form = RotinaForm(instance=rotina)

    return render(request, 'app/add_or_edit_rotina.html', {'form': form})


def delete_rotina(request, id):
    rotina = get_object_or_404(Rotina, id=id)
    rotina.delete()
    return redirect('listar_rotina')


def listar_rotina(request):
    rotinas = Rotina.objects.all()
    return render(request, 'app/list_rotina.html', {'rotinas': rotinas})


""" def minhas_rotinas(request):
    rotinas = Rotina.objects.all()
    return render(request, 'app/minhas_rotinas.html', {'rotinas': rotinas}) """


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
            novo_status.save()

            rotina.status = novo_status.status
            rotina.save()
            return redirect('minhas_rotinas')
    else:
        form = AtualizarStatusRotinaForm(initial={'data': timezone.now(
        ).date().strftime('%Y-%m-%d')}, instance=ultimo_status)

    return render(request, 'app/atualizar_status_rotina.html', {'form': form, 'rotina': rotina})


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


def add_descricao_relatorio(request):
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


def edit_descricao_relatorio(request, id):
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


def list_descricao_relatorio(request):
    descricoes = Descricao_relatorio.objects.all()
    return render(request, 'app/list_descricao_relatorio.html', {'descricoes': descricoes})


def gerencia_rotina(request):
    status_diarios = StatusDiarioRotina.objects.all()

    responsaveis = CustomUser.objects.all()
    setores = Setor.objects.all()
    descricoes = Descricao_relatorio.objects.all()
    prazos = Rotina.objects.values_list('prazo', flat=True).distinct()

    responsavel_query = request.GET.get('responsavel')
    setor_query = request.GET.get('setor')
    descricao_query = request.GET.get('descricao')
    prazo_query = request.GET.get('prazo')
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


def obter_status_para_data(rotina, dia):
    # Substitua esta lógica pela sua lógica específica para determinar o status
    # Por exemplo, você pode verificar se há um objeto de status que corresponde a esta rotina e data
    status = StatusDiarioRotina.objects.filter(
        rotina=rotina, data=dia).order_by('-data', '-id').first()
    if status:
        status_para_letra = {
            'PENDENTE': 'A',
            'REALIZADO_PRAZO': 'R',
            'PREVISAO_EXECUCAO': 'P',
            'REALIZADO_FORA_PRAZO': 'F',
            'INVENTARIO_GERAL': 'I',
            'JUSTIFICADO': 'J'
        }
        # Substitua 'algum_campo_status' pelo campo real do seu modelo
        return status_para_letra.get(status.status, '')
    else:
        # Ou qualquer valor padrão que você deseja mostrar se não houver status
        return ''


def get_dias_uteis(mes, ano):
    dias_do_mes = []
    data = datetime(ano, mes, 1)
    while data.month == mes:
        if data.weekday() < 5:  # 0-4 são dias de semana (segunda a sexta)
            dias_do_mes.append(data)
        data += timedelta(days=1)
    return dias_do_mes


def sua_view(request):
    ano_atual, mes_atual = datetime.now().year, datetime.now().month
    dias_do_mes = get_dias_uteis(mes_atual, ano_atual)
    rotinas = Rotina.objects.all().select_related(
        'responsavel').order_by('responsavel__fullname', 'created_at')

    rotinas_com_status = []
    for rotina in rotinas:
        status_diarios = [obter_status_para_data(
            rotina, dia) for dia in dias_do_mes]  # Substitua por sua lógica
        rotinas_com_status.append({
            'rotina': rotina,
            'status_diarios': status_diarios
        })

    return render(request, 'app/seu_template_calendario.html', {
        'rotinas_com_status': rotinas_com_status,
        'dias_do_mes': dias_do_mes
    })
