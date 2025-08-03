"""
URL configuration for todo_list_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken import views as auth_views


# OpenAPI-Schema-Ansicht für API-Dokumentation
schema_view = get_schema_view(
   openapi.Info(
      title="Todo API",
      default_version='v1',
      description="API for a simple Todo list application.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@todo.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # API-Endpunkte für die Todo-App
    path('api/todos/', include('todo_app.urls')),

    # REST Framework Login/Logout-Views für das browsable API
    path('api-auth/', include('rest_framework.urls')),
    
    # Token-basierter Login-Endpunkt von DRF
    path('api/auth/login/', auth_views.obtain_auth_token),

    # API-Dokumentation mit Swagger/OpenAPI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
