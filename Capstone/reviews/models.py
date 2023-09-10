from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Review(models.Model):

    rating_choices = ((1, "1 Star"), (2, "2 Stars"), (3, "3 Stars"), (4, "4 Start"), (5, "5 Start"), )
    experience_choices = (("employee", "employee"), ("interview", "interview"), ("coop", "COOP"), )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    experience = models.CharField(max_length=128, choices=experience_choices)
    position = models.CharField(max_length=256)
    description = models.TextField()
    publish_date = models.DateField()
    rating = models.IntegerField(choices=rating_choices)
    file = models.FileField(upload_to="pdfs/",blank=True)

