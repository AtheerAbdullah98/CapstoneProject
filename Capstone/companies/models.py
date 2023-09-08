from django.db import models

# Create your models here.
class Company(models.Model):

    name = models.CharField(max_length=2048)
    image = models.ImageField(upload_to="images/")
    field = models.CharField(max_length=2048)
    info= models.TextField()
    description = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return f"{self.name}"