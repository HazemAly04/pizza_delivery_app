from django.urls import path
from . import views
from .forms import *

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.UserSignupView.as_view(), name="register"),
    path('login/',views.LoginView.as_view(template_name="login.html", authentication_form=UserLoginForm), name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('pizza/', views.order_pizza, name="pizza"),
    path('order/<int:pizzaid>', views.order, name="order"),
    path('confirmation/<int:orderid>', views.confirmation, name='confirmation'),
    path('previous_orders/', views.previous_orders, name='previous_orders'),
]