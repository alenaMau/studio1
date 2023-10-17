from django.urls import re_path
from . import views
from .views import BBLoginView, delete_order
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
    re_path('delete_order/<uuid:order_id>/', delete_order, name='delete_order')

]

