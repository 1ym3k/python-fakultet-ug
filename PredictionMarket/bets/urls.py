from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    
    #gotowce od django do logowania i wylogowania:
    path('login/', auth_views.LoginView.as_view(template_name='bets/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cancel-bet/<int:bet_id>/', views.cancel_bet, name='cancel_bet'),
    path('chat-api/', views.chat_api, name='chat_api'),
]