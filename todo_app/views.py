from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Todo
from .serializers import TodoSerializer, UserSerializer

class TodoViewSet(viewsets.ModelViewSet):
    """
    Ein ViewSet für die Anzeige und Bearbeitung von To-Do-Einträgen.
    Stellt automatisch die Endpunkte für CRUD-Operationen bereit.
    """
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Gibt nur die To-Dos zurück, die dem authentifizierten Benutzer gehören.
        """
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Weist den erstellten To-Do-Eintrag automatisch dem aktuellen Benutzer zu.
        """
        serializer.save(user=self.request.user)

class UserViewSet(viewsets.ModelViewSet):
    """
    Ein ViewSet für die Benutzerregistrierung und das Auflisten von Benutzern (nur für Admin).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Setzt die Berechtigungen basierend auf der Aktion.
        Die Registrierung ist für jedermann erlaubt ('AllowAny').
        Andere Aktionen sind nur für authentifizierte Benutzer.
        """
        if self.action == 'create' or self.action == 'register':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        """
        Ein benutzerdefinierter Endpunkt für die Registrierung eines neuen Benutzers.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user": UserSerializer(user).data,
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)