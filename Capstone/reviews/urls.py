from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("add/", views.add_review_view, name="add_review_view"),
    path("all/", views.all_reviews_view, name="all_reviews_view"),

]