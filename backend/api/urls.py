from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Members
    path('members/', views.members, name='members'),
    path('members/<int:pk>/', views.member_detail, name='member_detail'),
    
    # Sacraments
    path('sacraments/', views.sacraments, name='sacraments'),
    path('sacraments/<int:pk>/', views.sacrament_detail, name='sacrament_detail'),
    
    # Pledges
    path('pledges/', views.pledges, name='pledges'),
    path('pledges/<int:pk>/', views.pledge_detail, name='pledge_detail'),
    
    # Payments
    path('payments/', views.payments, name='payments'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
]