from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.serve_index, name='home'),
    path('api/', include('api.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])