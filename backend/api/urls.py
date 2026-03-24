from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login, name='api_login'),
    path('logout/', views.logout, name='api_logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Members
    path('members/', views.members, name='members'),
    path('members/<int:pk>/', views.member_detail, name='member_detail'),
    
    # Debug
    path('debug-files/', views.debug_files, name='debug_files'),
]