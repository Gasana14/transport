
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('admin_dashboard', views.admin_dashboard, name="admin_dashboard"),
    path('customer_dashboard', views.customer_dashboard, name="customer_dashboard"),
    path('driver_dashboard', views.driver_dashboard, name="driver_dashboard"),
    path('register', views.register_account, name="register"),
    path('customer_login', views.login_client, name="login_client"),
    path('driver_login', views.login_driver, name="login_driver"),
    path('driver_missions', views.driver_missions, name="driver_missions"),
]
