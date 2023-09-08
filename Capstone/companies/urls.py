from django.urls import path
from . import views

app_name = "companies"

urlpatterns = [
     
    path("all/", views.all_companies_view, name="all_companies_view"),
    path("add/", views.add_company_view, name="add_company_view"),
    path("update/<company_id>/", views.company_update_view, name="company_update_view"),
    path("delete/<company_id>/", views.company_delete_view, name="company_delete_view"),
    path("detail/<company_id>/", views.company_detail_view, name="company_detail_view"),
]