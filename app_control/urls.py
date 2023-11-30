from django.urls import path
from .views import *

urlpatterns = [
    path('descricao_relatorio/add/', add_descricao_relatorio,
         name='add_descricao_relatorio'),
    path('descricao_relatorio/edit/<int:id>/',
         edit_descricao_relatorio, name='edit_descricao_relatorio'),
    path('descricao_relatorio/list/', list_descricao_relatorio,
         name='list_descricao_relatorio'),


    path('setor/add/', add_setor, name='add_setor'),
    path('setor/edit/<int:id>/', edit_setor, name='edit_setor'),
    path('setor/delete/<int:id>/', delete_setor, name='delete_setor'),
    path('setor/list', list_setor, name='list_setor'),


    path('responsavel/add/', add_responsavel, name='add_responsavel'),
    path('responsavel/edit/<int:id>/', edit_responsavel, name='edit_responsavel'),
    path('responsavel/delete/<int:id>/',
         delete_responsavel, name='delete_responsavel'),
    path('responsavel/list', list_responsavel, name='list_responsavel'),


    path('rotina/add/', add_rotina, name='add_rotina'),
    path('rotina/edit/<int:id>/', edit_rotina, name='edit_rotina'),
    path('rotina/delete/<int:id>/', delete_rotina, name='delete_rotina'),
    path('rotina/list', listar_rotina, name='listar_rotina'),
    path('minhas-rotinas/', minhas_rotinas, name='minhas_rotinas'),
    path('rotina/atualizar-status/<int:pk>/', atualizar_status_rotina, name='atualizar_status_rotina'),
]
