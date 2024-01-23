from django import forms
from django.core.validators import RegexValidator
from .models import User, Category, Status
from django.core.exceptions import ValidationError
from django import forms
from .models import Order


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             label='Адрес электронной почты')

    class Meta:
        model = User
        fields = ('fio', 'email', 'password', 'login')


class RegisterUserForm(forms.ModelForm):
    fio = forms.CharField(label='ФИО')
    email = forms.EmailField(required=True,
                             label='Адрес электронной почты')
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Пароль (повторно)',
                                widget=forms.PasswordInput,
                                help_text='Повторите тот же самый пароль еще раз')
    access = forms.BooleanField(required=True, label='Согласие на обработку персональных данных')
    login = forms.CharField(required=True, label='Логин', validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9]+$',
                message='Логин должен содержать только латинские буквы и цифры.',
                code='invalid_login'
            )
        ])

    def clean(self):
        super().clean()
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password and password2 and password != password2:
            errors = {'password2': ValidationError(
                'Введенные пароли не совпадают', code='password_mismatch'
            )}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['login']
        user.fio = self.cleaned_data['fio']
        user.is_active = True
        user.is_activated = True
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('fio', 'login', 'email', 'password', 'password2', 'access')


class OrderCreationForm(forms.ModelForm):
    user = None

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(OrderCreationForm, self).__init__(*args, **kwargs)

    name = forms.CharField(required=True, label='Название')
    description = forms.CharField(required=True, label='Описание')
    category = forms.ModelChoiceField(required=True, queryset=Category.objects.all().order_by('name'))
    photo = forms.ImageField(required=True, label='Фото', widget=forms.ClearableFileInput)

    def clean(self):
        super().clean()

    def save(self, commit=True):
        order = super().save(commit=False)
        order.name = self.cleaned_data['name']
        order.description = self.cleaned_data['description']
        order.category_id = self.cleaned_data['category']
        status_model = Status.objects.get(name='Новое')
        order.status_id = status_model
        order.user_id = self.user
        if 'photo' in self.files:
            uploaded_photo = self.files['photo']
            order.save_uploaded_photo(uploaded_photo)

        if commit:
            order.save()
        return order

    class Meta:
        model = Order
        fields = ('name', 'description', 'category', 'photo')


class StatusFilterForm(forms.Form):
    status = forms.ModelChoiceField(queryset=Status.objects.all(), empty_label="Выберите статус", required=False)

    class Meta:
        model = Status
        fields = ('status')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'description', 'category_id', 'status_id', 'photo', 'comment']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class DeleteCategoryForm(forms.Form):
    category_id = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)
