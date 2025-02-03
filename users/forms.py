from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from users.models import Company, UserProfile


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', help_text='Максимум 150 символов', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserRegisterCompany(UserCreationForm):
    company = forms.CharField(label='Название компании', help_text='Максимум 150 символов', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}))
    username = forms.CharField(label='Имя пользователя', help_text='Максимум 150 символов', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean_company(self):
        """ Проверка, существует ли компания """
        company_name = self.cleaned_data.get('company')

        # Проверяем, есть ли такая компания
        if Company.objects.filter(name__iexact=company_name).exists():
            raise ValidationError("Компания с таким названием уже зарегистрирована. "
                                  "Если вы сотрудник, попросите администратора компании создать вам аккаунт.")

        return company_name

    class Meta:
        model = User
        fields = ('company', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        """ Сохранение пользователя и создание компании """
        user = super().save(commit=False)  # Создаём пользователя, но пока не сохраняем

        # Получаем название компании
        company_name = self.cleaned_data['company']

        # Создаём компанию (ошибка невозможна, так как clean_company не пропустит дубликаты)
        company_obj = Company.objects.create(name=company_name)

        if commit:
            user.save()  # Сохраняем пользователя
            UserProfile.objects.create(user=user, company=company_obj)  # Привязываем пользователя к компании
        return user
