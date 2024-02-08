from django.http import HttpResponseForbidden
from .models import CustomUser, UserActivities, Setor
from django.shortcuts import redirect, render, get_object_or_404
from .forms.usuario_forms import CadastroUsuarioForm, CadastroUsuarioAdministradorForm, EditarUsuarioForm, SetorForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required



def add_user_activity(user, action):
  UserActivities.objects.create(
      user_id=user.id,
      email=user.email,
      fullname=user.fullname,
      action=action
)

# Create your views here.
@login_required
def cadastrar_usuario(request):
  if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado. Você precisa ser administrador.")
  if request.method == "POST":
    form_usuario = CadastroUsuarioForm(request.POST)
    form_usuario.fields['fullname'].label = "Nome"
    if form_usuario.is_valid():
      form_usuario.save()
      return redirect('listar_usuarios')
  else:
    form_usuario = CadastroUsuarioForm()
  return render(request, 'usuarios/form_usuario.html', {'form_usuario': form_usuario})

@login_required
def cadastrar_usuario_administrador(request):
  if not request.user.is_superuser:
        return HttpResponseForbidden("Acesso negado. Você precisa ser administrador.")
  if request.method == "POST":
    form_usuario = CadastroUsuarioAdministradorForm(request.POST)
    form_usuario.fields['fullname'].label = "Nome"
    if form_usuario.is_valid():
      form_usuario.save()
      return redirect('listar_usuarios')
  else:
    form_usuario = CadastroUsuarioForm()
  return render(request, 'usuarios/form_usuario.html', {'form_usuario': form_usuario})

@login_required
def listar_usuarios(request):
  if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado. Você precisa ser administrador.")
  User = get_user_model()
  usuarios = User.objects.all()
  return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

@login_required
def editar_usuario(request, id):
  if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado. Você precisa ser administrador.")
  User = get_user_model()
  usuario = User.objects.get(id=id)
  form_usuario = EditarUsuarioForm(request.POST or None, instance=usuario)
  form_usuario.fields['fullname'].label = "Nome"

  if form_usuario.is_valid():
    form_usuario.save()
    return redirect('listar_usuarios')
  return render(request, 'usuarios/form_usuario.html', {'form_usuario': form_usuario})

@login_required
def deletar_usuario(request, id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado. Você precisa ser administrador.")

    User = get_user_model()
    usuario = get_object_or_404(User, id=id)

    if usuario.is_superuser:
        if not request.user.is_superuser:
            return HttpResponseForbidden("Acesso negado. Não é possível deletar um superusuário.")

    usuario.delete()
    return redirect('listar_usuarios')

@login_required
def add_setor(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado. Você precisa ser administrador.")
    if request.method == 'POST':
        form = SetorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_setor')
    else:
        form = SetorForm()

    return render(request, 'app/add_or_edit_setor.html', {'form': form})

@login_required
def edit_setor(request, id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado. Você precisa ser administrador.")
    setor = Setor.objects.get(id=id)
    if request.method == 'POST':
        form = SetorForm(request.POST, instance=setor)
        if form.is_valid():
            form.save()
            return redirect('')
    else:
        form = SetorForm(instance=setor)

    return render(request, 'app/add_or_edit_setor.html', {'form': form})

@login_required
def list_setor(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado. Você precisa ser administrador.")
    setores = Setor.objects.all()
    return render(request, 'app/list_setor.html', {'setores': setores})


def delete_setor(request, id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado. Você precisa ser administrador.")
    setor = get_object_or_404(Setor, id=id)
    setor.delete()
    return redirect('list_setor')