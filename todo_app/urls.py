from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet, UserViewSet

# Erstellt einen Router, um URLs automatisch für die ViewSets zu generieren
router = DefaultRouter()
router.register(r'list', TodoViewSet, basename='todos')
router.register(r'users', UserViewSet)

urlpatterns = [
    # Enthält alle von den ViewSets generierten URLs
    path('', include(router.urls)),
]