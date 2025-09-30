from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Petition(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    yes_votes = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title