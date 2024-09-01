from django.urls import path     
from . import views

urlpatterns = [
     path('', views.index),
     path('login', views.login, name='login'),
     path('register/', views.register, name='register'),
     path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
     path('create_session/<int:coach_id>/', views.create_session, name='create_session'),
     path('update_session/<int:session_id>/', views.update_session, name='update_session'),
]