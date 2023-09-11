from django.urls import path
from . import views

app_name = "companies"

urlpatterns = [
     
    path("all/", views.all_companies_view, name="all_companies_view"),
    path("add/", views.add_company_view, name="add_company_view"),
    path("update/<company_id>/", views.company_update_view, name="company_update_view"),
    path("delete/<company_id>/", views.company_delete_view, name="company_delete_view"),
    path("detail/<company_id>/", views.company_detail_view, name="company_detail_view"),
    path("search/",views.companies_search_view, name="companies_search_view"),
    path("approve/",views.approve_company_view, name="approve_company_view"),
    path("reveiw/add/<company_id>/",views.add_Review_view,name="add_Review_view"),
    path("reveiw/delete/<review_id>/",views.review_delete_view,name="review_delete_view"),
    path("reveiw/update/<review_id>/", views.review_update_view, name="review_update_view"),
    path("reveiw/all/", views.all_reveiws_view, name="all_reveiws_view"),
]