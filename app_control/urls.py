from django.urls import path
from .views import *

urlpatterns = [
  path('descricao_relatorio/add/', add_descricao_relatorio, name='add_descricao_relatorio'),
  path('descricao_relatorio/edit/<int:id>/', edit_descricao_relatorio, name='edit_descricao_relatorio'),
  path('descricao_relatorio/list/', list_descricao_relatorio, name='list_descricao_relatorio'),


  path('rotina/add/', add_rotina, name='add_rotina'),
  path('rotina/edit/<int:id>/', edit_rotina, name='edit_rotina'),
  path('rotina/delete/<int:id>/', delete_rotina, name='delete_rotina'),
]