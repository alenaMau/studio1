from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from studio.studio import settings
from .forms import ChangeUserInfoForm, StatusFilterForm
from .models import User, Order, Status
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import CreateView
from .forms import RegisterUserForm
from django.views.generic import TemplateView
from .forms import OrderCreationForm


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
