"""URLs raiz do projeto Get a Pet."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Admin do Django
    path('admin/', admin.site.urls),

    # --- Documentação da API (Swagger em /api/docs/) ---
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # --- API REST ---
    path('api/users/', include('apps.users.urls')),
    path('api/pets/', include('apps.pets.urls')),

    # --- Views de template (frontend HTML) ---
    path('', include('apps.pets.template_urls')),
    path('users/', include('apps.users.template_urls')),
]

# Serve arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
