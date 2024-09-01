from django.urls import path     
from . import views

urlpatterns = [
     path('', views.index),
     path('login', views.login, name='login'),
     path('register/', views.register, name='register'),
     path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
     path('create_session/<int:coach_id>/', views.create_session, name='create_session'),
     path('update_session/<int:session_id>/', views.update_session, name='update_session'),
     path('cancel_session/<int:session_id>/', views.cancel_session, name='cancel_session'),
     path('create_review/<int:coach_id>/', views.create_review, name='create_review'),
     path('update_review/<int:review_id>/', views.update_review, name='update_review'),
     path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
     path('logout/', views.logout_user, name='logout_user'),
     path('about_us/', views.about_us, name='about_us'),
     path('terms/', views.terms_of_use, name='terms_of_use'),
     path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
     path('upcoming_sessions/', views.upcoming_sessions, name='upcoming_sessions'),
     path('recent_reviews/', views.recent_reviews, name='recent_reviews'),
]