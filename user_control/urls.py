from django.urls import path, reverse_lazy
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('cadastrar', cadastrar_usuario, name='cadastrar_usuario'),
    path('listar', listar_usuarios, name='listar_usuarios'),
    path('editar/<int:id>', editar_usuario, name='editar_usuario'),
    path('deletar/<int:id>', deletar_usuario, name='deletar_usuario'),
    path('login', auth_views.LoginView.as_view(), name='logar_usuario'),
    path('logout', auth_views.LogoutView.as_view(), name='deslogar_usuario'),
    path('alterar_senha', auth_views.PasswordChangeView.as_view(
        success_url=reverse_lazy('listar_usuarios')), name='alterar_senha'),
]
