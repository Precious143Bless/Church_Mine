from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.serve_index, name='home'),
    path('login.html', views.serve_html, {'filename': 'login.html'}, name='login'),
    path('dashboard.html', views.serve_html, {'filename': 'dashboard.html'}, name='dashboard'),
    path('members.html', views.serve_html, {'filename': 'members.html'}, name='members'),
    path('member-detail.html', views.serve_html, {'filename': 'member-detail.html'}, name='member_detail'),
    path('member-form.html', views.serve_html, {'filename': 'member-form.html'}, name='member_form'),
    path('sacraments.html', views.serve_html, {'filename': 'sacraments.html'}, name='sacraments'),
    path('pledges.html', views.serve_html, {'filename': 'pledges.html'}, name='pledges'),
    path('payments.html', views.serve_html, {'filename': 'payments.html'}, name='payments'),
    path('reports.html', views.serve_html, {'filename': 'reports.html'}, name='reports'),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)