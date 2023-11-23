from django.urls import path
from .views import *

urlpatterns = [
  path('cadastrar', cadastrar_usuario, name='cadastrar_usuario'),
  path('listar', listar_usuarios, name='listar_usuarios'),
  path('editar/<int:id>', editar_usuario, name='editar_usuario'),
  path('deletar/<int:id>', deletar_usuario, name='deletar_usuario'),
]