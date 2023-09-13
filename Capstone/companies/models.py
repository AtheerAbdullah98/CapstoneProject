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
    

class Review(models.Model):

    rating_choices = ((1, "1 Star"), (2, "2 Stars"), (3, "3 Stars"), (4, "4 Start"), (5, "5 Start"), )
    experience_choices = (("موظف", "موظف"), ("مقابلة", "مقابلة"), ("تدريب", "تدريب"), )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    experience = models.CharField(max_length=128, choices=experience_choices)
    position = models.CharField(max_length=256)
    description = models.TextField()
    publish_date = models.DateField(auto_now_add=True)
    rating = models.IntegerField(choices=rating_choices)



    def __str__(self):
        return f"{self.user.first_name} on {self.company.name}"

class Favorite(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.review} on {self.review}"

class Report(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.review} on {self.review}"