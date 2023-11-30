from django.shortcuts import get_object_or_404, render, redirect
from .forms.app_forms import AtualizarStatusRotinaForm, RotinaForm, DescricaoRelatorioForm, SetorForm, ResponsavelForm
from .models import Rotina, Descricao_relatorio, Setor, Responsavel, StatusDiarioRotina
from django.utils import timezone

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
    data_atual = timezone.now().date()

    # Obter o último status para a data atual, se existir
    ultimo_status = StatusDiarioRotina.objects.filter(rotina=rotina, data=data_atual).order_by('-id').first()

    if request.method == 'POST':
        form = AtualizarStatusRotinaForm(request.POST)
        if form.is_valid():
            # Criar um novo registro de status diário
            novo_status = form.save(commit=False)
            novo_status.rotina = rotina
            novo_status.data = data_atual
            novo_status.usuario = request.user
            novo_status.save()

            # Opcional: Atualizar o status na tabela Rotina
            rotina.status = novo_status.status
            rotina.save()
            return redirect('minhas_rotinas')
    else:
        # Inicializar o formulário com o último status, se existir
        form = AtualizarStatusRotinaForm(instance=ultimo_status)

    return render(request, 'app/atualizar_status_rotina.html', {'form': form, 'rotina': rotina})


def minhas_rotinas(request):
    data_atual = timezone.now().date()
    rotinas = Rotina.objects.filter(responsavel=request.user)
    status = StatusDiarioRotina.objects.filter(rotina__in=rotinas, data=data_atual)
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

# Setor


def add_setor(request):
    if request.method == 'POST':
        form = SetorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_setor')
    else:
        form = SetorForm()

    return render(request, 'app/add_or_edit_setor.html', {'form': form})


def edit_setor(request, id):
    setor = Setor.objects.get(id=id)
    if request.method == 'POST':
        form = SetorForm(request.POST, instance=setor)
        if form.is_valid():
            form.save()
            return redirect('')
    else:
        form = SetorForm(instance=setor)

    return render(request, 'app/add_or_edit_setor.html', {'form': form})


def list_setor(request):
    setores = Setor.objects.all()
    return render(request, 'app/list_setor.html', {'setores': setores})


def delete_setor(request, id):
    setor = get_object_or_404(Setor, id=id)
    setor.delete()
    return redirect('list_setor')

# Responsavel


def add_responsavel(request):
    if request.method == 'POST':
        form = ResponsavelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_responsavel')
    else:
        form = ResponsavelForm()

    return render(request, 'app/add_or_edit_responsavel.html', {'form': form})


def edit_responsavel(request, id):
    responsavel = Responsavel.objects.get(id=id)
    if request.method == 'POST':
        form = ResponsavelForm(request.POST, instance=responsavel)
        if form.is_valid():
            return redirect('')
    else:
        form = ResponsavelForm(instantece=responsavel)

    return render(request, 'app/add_or_edit_setor.html', {'form': form})


def list_responsavel(request):
    responsaveis = Responsavel.objects.all()
    return render(request, 'app/list_responsavel.html', {'responsaveis': responsaveis})


def delete_responsavel(request, id):
    responsavel = get_object_or_404(Responsavel, id=id)
    responsavel.delete()
    return redirect('list_responsavel')
