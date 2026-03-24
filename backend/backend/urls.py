from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Serve the main index.html
    path('', views.serve_index, name='home'),
    
    # Serve all HTML files from frontend folder
    path('login.html', views.serve_html, {'filename': 'login.html'}, name='login'),
    path('dashboard.html', views.serve_html, {'filename': 'dashboard.html'}, name='dashboard'),
    path('members.html', views.serve_html, {'filename': 'members.html'}, name='members'),
    path('member-detail.html', views.serve_html, {'filename': 'member-detail.html'}, name='member_detail'),
    path('member-form.html', views.serve_html, {'filename': 'member-form.html'}, name='member_form'),
    path('sacraments.html', views.serve_html, {'filename': 'sacraments.html'}, name='sacraments'),
    path('pledges.html', views.serve_html, {'filename': 'pledges.html'}, name='pledges'),
    path('payments.html', views.serve_html, {'filename': 'payments.html'}, name='payments'),
    path('reports.html', views.serve_html, {'filename': 'reports.html'}, name='reports'),
    
    # API endpoints
    path('api/', include('api.urls')),
]

# Serve static files (CSS, JS) in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])