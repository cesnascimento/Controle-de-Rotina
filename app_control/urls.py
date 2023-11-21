from django.urls import path
from .views import exemplo

urlpatterns = [
  path('exemplo', exemplo, name='exemplo')
]