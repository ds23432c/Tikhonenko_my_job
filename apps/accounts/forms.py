from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, AVATAR_CHOICES, THEME_CHOICES


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'почта@пример.ру'}))
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ваш_ник'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.setdefault('class', 'form-control')


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'почта@пример.ру'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '••••••••'}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'bio', 'avatar_emoji', 'theme']
        labels = {
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'bio': 'О себе',
            'avatar_emoji': 'Аватар',
            'theme': 'Тема',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'avatar_emoji': forms.Select(attrs={'class': 'form-select'}),
            'theme': forms.Select(attrs={'class': 'form-select'}),
        }
