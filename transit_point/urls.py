from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView  # Добавьте этот импорт
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Pereval API",
        default_version='v1',
        description="API для работы с данными о перевалах",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('pereval.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Добавьте этот маршрут для главной страницы
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]