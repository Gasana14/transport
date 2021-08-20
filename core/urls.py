
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('login_page', views.login_page, name='login_page'),
    path('record_new_carriage', views.record_new_carriage, name="record_new_carriage"),
    path('admin_dashboard', views.admin_dashboard, name="admin_dashboard"),
    path('customer_dashboard', views.customer_dashboard, name="customer_dashboard"),
    path('driver_dashboard', views.driver_dashboard, name="driver_dashboard"),
    path('register', views.register_account, name="register"),
    path('customer_login', views.login_client, name="login_client"),
    path('driver_login', views.login_driver, name="login_driver"),
    path('driver_missions', views.driver_missions, name="driver_missions"),
    path('register_page', views.register_page, name="register_page")
]
