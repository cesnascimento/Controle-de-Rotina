from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from ..models import Setor

class CadastroUsuarioForm(UserCreationForm):
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.is_superuser = True
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['fullname', 'email' , 'setor', 'password1', 'password2']
        labels = {'fullname': 'Nome'}
 

class EditarUsuarioForm(UserChangeForm):
    password = None

    class Meta:
        model = get_user_model()
        fields = ['fullname', 'email', 'setor']
        labels = {'fullname': 'Nome'}


class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        fields = ['sector']
        labels = {'sector': 'Setor'}