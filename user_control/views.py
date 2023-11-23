from .models import CustomUser
from django.shortcuts import redirect, render, get_object_or_404
from .forms.usuario_forms import CadastroUsuarioForm, EditarUsuarioForm
from django.contrib.auth import get_user_model

# Create your views here.
def cadastrar_usuario(request):
  if request.method == "POST":
    form_usuario = CadastroUsuarioForm(request.POST)
    form_usuario.fields['fullname'].label = "Nome"
    if form_usuario.is_valid():
      form_usuario.save()
      return redirect('listar_usuarios')
  else:
    form_usuario = CadastroUsuarioForm()
  return render(request, 'usuarios/form_usuario.html', {'form_usuario': form_usuario})


def listar_usuarios(request):
  User = get_user_model()
  usuarios = User.objects.all()
  return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

def editar_usuario(request, id):
  User = get_user_model()
  usuario = User.objects.get(id=id)
  form_usuario = EditarUsuarioForm(request.POST or None, instance=usuario)
  form_usuario.fields['fullname'].label = "Nome"

  if form_usuario.is_valid():
    form_usuario.save()
    return redirect('listar_usuarios')
  return render(request, 'usuarios/form_usuario.html', {'form_usuario': form_usuario})

def deletar_usuario(request, id):
  User = get_user_model()
  usuario = User.objects.get(id=id)
  usuario.delete()
  return redirect('listar_usuarios')

 