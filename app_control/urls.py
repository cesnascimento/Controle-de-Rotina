from django.urls import path
from .views import *

urlpatterns = [
    path('descricao_relatorio/add/', add_descricao_relatorio,
         name='add_descricao_relatorio'),
    path('descricao_relatorio/edit/<int:id>/',
         edit_descricao_relatorio, name='edit_descricao_relatorio'),
    path('descricao_relatorio/list/', list_descricao_relatorio,
         name='list_descricao_relatorio'),


    path('rotina/add/', add_rotina, name='add_rotina'),
    path('rotina/edit/<int:id>/', edit_rotina, name='edit_rotina'),
    path('rotina/delete/<int:id>/', delete_rotina, name='delete_rotina'),
    path('rotina/list', listar_rotina, name='listar_rotina'),
    path('minhas-rotinas/', minhas_rotinas, name='minhas_rotinas'),
    path('rotina/atualizar-status/<int:pk>/', atualizar_status_rotina, name='atualizar_status_rotina'),
    path('gerencia-rotinas', gerencia_rotina, name='gerencia_rotinas'),
]
