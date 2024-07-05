from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns




schema_view = get_schema_view(
    openapi.Info(
        title="Job Portal API",
        default_version='v1',
        description="Playground For Job Portal API",
        # schemes=None
    ),
    public=True,
    # schemes=("http", "https"),
    permission_classes=(permissions.AllowAny,),
    # authentication_classes=(JWTAuthentication,)
)


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('api/', include('core_apps.users.urls', namespace='users')),
    path('api/', include('core_apps.profiles.urls', namespace='profiles')),
    path('', include('core_apps.jobapp.urls', namespace="job_app")),

    path('docs(<format>\.json|\.yaml)/', schema_view.without_ui(
        cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger',
                                        cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                         cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()