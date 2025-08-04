from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Todo

class UserSerializer(serializers.ModelSerializer):
    """
    Ein Serializer für die Benutzerregistrierung.
    Erstellt einen neuen Benutzer mit einem gehashten Passwort.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class TodoSerializer(serializers.ModelSerializer):
    """
    Ein Serializer für das To-Do-Modell.
    Stellt sicher, dass das 'user'-Feld schreibgeschützt ist
    und automatisch auf den aktuellen Benutzer gesetzt wird.
    """
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Todo
        fields = ('id', 'user', 'title', 'description', 'is_completed', 'created_at', 'updated_at')
