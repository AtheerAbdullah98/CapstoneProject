from django.urls import path
from . import views

app_name = "companies"

urlpatterns = [
    path('add/', views.add_company_view, name="add_company_view"),
]