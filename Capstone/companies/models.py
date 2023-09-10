from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Company(models.Model):

    name = models.CharField(max_length=2048)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/")
    field = models.CharField(max_length=2048)
    info= models.TextField()
    description = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

   
    def __str__(self):
        return f"{self.name}"