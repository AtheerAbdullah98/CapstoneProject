from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=2048, blank=True)
    birth_date = models.DateField(default="2095-1-1")
    avatar = models.ImageField(upload_to="images/", default="images/default-avatar.png")
    twitter_link = models.URLField(blank=True)


    def __str__(self) -> str:
        return f"{self.user.username} profile"
