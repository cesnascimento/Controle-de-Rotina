from django.shortcuts import get_object_or_404, render, redirect
from .forms.app_forms import RotinaForm, DescricaoRelatorioForm
from .models import Rotina, Descricao_relatorio


def add_rotina(request):
    if request.method == 'POST':
        form = RotinaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('url_para_lista_de_rotinas')  # Substitua pela URL desejada
    else:
        form = RotinaForm()

    return render(request, 'app/add_or_edit_rotina.html', {'form': form})


def edit_rotina(request, id):
    rotina = Rotina.objects.get(id=id)
    if request.method == 'POST':
        form = RotinaForm(request.POST, instance=rotina)
        if form.is_valid():
            form.save()
            return redirect('url_para_lista_de_rotinas')
    else:
        form = RotinaForm(instance=rotina)

    return render(request, 'app/add_or_edit_rotina.html', {'form': form})


def delete_rotina(request, id):
    rotina = get_object_or_404(Rotina, id=id)
    rotina.delete()
    return redirect('url_para_lista_de_rotinas')


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
        form_descricao_relatorio = DescricaoRelatorioForm(request.POST, instance=descricao_relatorio)
        if form_descricao_relatorio.is_valid():
            form_descricao_relatorio.save()
            return redirect('list_descricao_relatorio')
    else:
        form_descricao_relatorio = DescricaoRelatorioForm(instance=descricao_relatorio)

    return render(request, 'app/add_descricao_relatorio.html', {'form_descricao_relatorio': form_descricao_relatorio, 'descricao_relatorio': descricao_relatorio})

def list_descricao_relatorio(request):
    descricoes = Descricao_relatorio.objects.all()
    return render(request, 'app/list_descricao_relatorio.html', {'descricoes': descricoes})