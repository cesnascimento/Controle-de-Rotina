from django import forms
from django.contrib.auth.forms import UserCreationForm
from user_control.models import CustomUser

class UsuarioForm(UserCreationForm):

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.is_superuser = True
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('fullname', 'email' ,'password1', 'password2')
