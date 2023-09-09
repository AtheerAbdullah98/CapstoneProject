from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Review

# Create your views here.
def add_review_view(request: HttpRequest):
          
    if request.method == "POST":
            new_review = Review(experience=request.POST["experience"], position=request.POST["position"], description=request.POST["description"], publish_date=request.POST["publish_date"], rating= request.POST["rating"],file=request.FILES["file"])
            new_review.save()

            return redirect("reviews:all_reviews_view")

    return render(request, 'reviews/add_review.html', {"Review": Review})



def all_reviews_view(request: HttpRequest):
        
    reviews = Review.objects.all()

    return render(request, "reviews/all_reviews.html", context = {"reviews" : reviews})




