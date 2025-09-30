from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from movies.models import Movie

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.user.username

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie,
        on_delete=models.CASCADE)
    order = models.ForeignKey(Order,
        on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

class UserFeedback(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255)
    experience = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"