from django.urls import re_path, path
from . import views
from .views import BBLoginView, delete_order, order_edit, order_list, delete_order_admin, add_category, delete_category
from .views import BBLogoutView
from .views import profile
from .views import ChangeUserView
from .views import BBPasswordChangeView
from .views import RegisterDoneView, RegisterUserView
from .views import OrderCreationView

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path('accounts/login', BBLoginView.as_view(), name='login'),
    re_path('accounts/profile/', profile, name='profile'),
    re_path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    re_path('accounts/profile/change/', ChangeUserView.as_view(), name='profile_change'),
    re_path('accounts/profile/', profile, name='profile'),
    re_path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    re_path('accounts/register/', RegisterUserView.as_view(), name='register'),
    re_path('accounts/password/change/', BBPasswordChangeView.as_view(), name='password_change'),
    re_path('accounts/order/creation/', OrderCreationView.as_view(), name='order_creation'),
    re_path(r'^order/$', OrderCreationView.as_view(), name='order'),
    path('add_category/', add_category, name='add_category'),
    path('delete_category/', delete_category, name='delete_category'),
    re_path('orders/list', order_list, name='order_list'),
    re_path('delete_order/<uuid:order_id>/', delete_order, name='delete_order'),
    re_path('delete_order_admin/<uuid:order_id>/', delete_order_admin, name='delete_order_admin'),
    path('orders/edit/<uuid:order_id>/', order_edit, name='order_edit')
]

