from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('regist/', views.registration, name='registration'),
    path('auth/login', views.auth_login, name='login'),
    path('auth/logout', views.auth_logout, name='logout'),
]
