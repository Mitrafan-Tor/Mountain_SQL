from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Pereval API",
        default_version='v1',
        description="API для работы с перевалами",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@pereval.local"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', RedirectView.as_view(url='/swagger/', permanent=False)),  # Перенаправление на Swagger
    path('admin/', admin.site.urls),
    path('api/', include('pereval.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]