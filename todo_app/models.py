from django.db import models
from django.conf import settings

class Todo(models.Model):
    """
    Ein To-Do-Modell, das mit einem bestimmten Benutzer verknüpft ist.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='todos'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"