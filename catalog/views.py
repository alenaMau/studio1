from django.core.checks import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from studio.studio import settings
from .forms import ChangeUserInfoForm, StatusFilterForm, CategoryForm, DeleteCategoryForm
from .models import User, Order, Status, Category
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import CreateView
from .forms import RegisterUserForm
from django.views.generic import TemplateView
from .forms import OrderCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from .forms import OrderForm
from django.contrib import messages


# Create your views here.

def index(request):
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL
    order_list = Order.objects.filter(status_id__name='Выполнено').order_by('-date')[:4]
    count_orders = Order.objects.filter(status_id__name='Принято в работу').count()
    return render(request, 'main/index.html',
                  {'count_orders': count_orders, 'order_list': order_list, 'media_root': media_root,
                   'media_url': media_url})


def delete_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        if order.user_id != request.user:
            return redirect('profile')
        order.delete()
    return redirect('profile')


def delete_order_admin(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        user = get_object_or_404(User, id=request.user.id)
        if user.is_superuser:
            order.delete()
    return redirect('order_list')


def order_edit(request, order_id=None):
    if order_id is not None:
        order = get_object_or_404(Order, id=order_id)
    else:
        order = None

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            if order:
                order.delete()
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)

    return render(request, 'main/order_edit.html', {'form': form})


def order_list(request):
    if request.user.is_superuser != True:
        return redirect('index')

    orders = Order.objects.all()
    return render(request, 'main/order_list.html', {'orders': orders})


def add_category(request):
    if request.user.is_superuser != True:
        return redirect('index')

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Добавление прошло успешно.')
    else:
        form = CategoryForm()

    return render(request, 'main/add_category.html', {'form': form})


def delete_category(request):
    if request.user.is_superuser != True:
        return redirect('index')

    if request.method == 'POST':
        form = DeleteCategoryForm(request.POST)
        if form.is_valid():
            category_id = form.cleaned_data['category_id'].id
            category = get_object_or_404(Category, id=category_id)
            category.delete()
            messages.success(request, 'Удаление прошло успешно.')
    else:
        form = DeleteCategoryForm()

    return render(request, 'main/delete_category.html', {'form': form})


class BBLoginView(LoginView):
    template_name = 'main/login.html'


@login_required
def account(required):
    return render(required, 'main/profile.html')


@login_required
def profile(request):
    orders = Order.objects.filter(user_id=request.user).order_by('-date')
    form = StatusFilterForm()
    if request.method == 'POST':
        form = StatusFilterForm(request.POST)
        if form.is_valid():
            selected_status = form.cleaned_data['status']
            if selected_status is not None:
                orders = orders.filter(status_id=selected_status)
    return render(request, 'main/profile.html', {'orders': orders, 'form': form})


class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


class ChangeUserView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'main/change_user.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('profile')
    success_message = 'Личные данные пользователя изменены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class BBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin,
                           PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('profile')
    success_message = 'Пароль пользователя изменен'


class RegisterUserView(CreateView):
    model = User
    template_name = 'main/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')


class OrderCreationView(CreateView):
    model = Order
    template_name = 'main/order_creation.html'
    form_class = OrderCreationForm
    success_url = reverse_lazy('profile')

    def get_form_kwargs(self):
        kwargs = super(OrderCreationView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class RegisterDoneView(TemplateView):
    template_name = 'main/register_completed.html'
