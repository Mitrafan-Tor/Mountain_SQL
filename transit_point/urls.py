from django.urls import path, include
from django.views.generic import TemplateView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Pereval API",
        default_version='v1',
        description="API для работы с перевалами",
        contact=openapi.Contact(email="contact@example.com"),
    public=True,),
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'),),
    path('api-endpoints/', TemplateView.as_view(template_name='api_endpoints.html'), name='api-endpoints'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include('pereval.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)