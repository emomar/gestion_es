from django import forms
from .models import Sortie, Enregistrement
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm, PasswordResetForm, UsernameField
from django.contrib.auth.models import User
class EnregistrementcreateForm(forms.ModelForm):
    
    class Meta:
        model = Enregistrement
        fields = '__all__'

        
class SortieCreateForm(forms.ModelForm):
    class Meta:
          model = Sortie
          fields =['enregistrement', 'Date_heure_sortie']


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nom Utilisateur'
    }))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Mot De Passe'
    }))