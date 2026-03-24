from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.serve_index, name='home'),
    path('test-frontend/', views.test_frontend, name='test_frontend'),  # Add this test URL
    
    # Serve HTML files directly from frontend folder
    path('login.html', TemplateView.as_view(template_name='login.html'), name='login_page'),
    path('dashboard.html', TemplateView.as_view(template_name='dashboard.html'), name='dashboard_page'),
    path('members.html', TemplateView.as_view(template_name='members.html'), name='members_page'),
    path('member-detail.html', TemplateView.as_view(template_name='member-detail.html'), name='member_detail_page'),
    path('member-form.html', TemplateView.as_view(template_name='member-form.html'), name='member_form_page'),
    path('sacraments.html', TemplateView.as_view(template_name='sacraments.html'), name='sacraments_page'),
    path('sacrament-form.html', TemplateView.as_view(template_name='sacrament-form.html'), name='sacrament_form_page'),
    path('pledges.html', TemplateView.as_view(template_name='pledges.html'), name='pledges_page'),
    path('pledge-form.html', TemplateView.as_view(template_name='pledge-form.html'), name='pledge_form_page'),
    path('payments.html', TemplateView.as_view(template_name='payments.html'), name='payments_page'),
    path('reports.html', TemplateView.as_view(template_name='reports.html'), name='reports_page'),
    
    path('api/', include('api.urls')),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])