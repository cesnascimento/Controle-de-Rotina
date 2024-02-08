from django.urls import path, reverse_lazy
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('cadastrar', cadastrar_usuario, name='cadastrar_usuario'),
    path('cadastraradministrador', cadastrar_usuario_administrador, name='cadastrar_usuario_administrador'),
    path('listar', listar_usuarios, name='listar_usuarios'),
    path('editar/<int:id>', editar_usuario, name='editar_usuario'),
    path('deletar/<int:id>', deletar_usuario, name='deletar_usuario'),
    path('login', auth_views.LoginView.as_view(), name='logar_usuario'),
    path('logout', auth_views.LogoutView.as_view(), name='deslogar_usuario'),
    path('alterar_senha', auth_views.PasswordChangeView.as_view(
        success_url=reverse_lazy('listar_usuarios')), name='alterar_senha'),

    path('setor/add/', add_setor, name='add_setor'),
    path('setor/edit/<int:id>/', edit_setor, name='edit_setor'),
    path('setor/delete/<int:id>/', delete_setor, name='delete_setor'),
    path('setor/list', list_setor, name='list_setor'),
]
