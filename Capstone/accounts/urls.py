from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register_user_view, name="register_user_view"),
    path("login/", views.login_user_view, name="login_user_view"),
    path("logout/", views.logout_user_view, name="logout_user_view"),
    path('profile/<user_id>/', views.profile_page, name="profile_page"),
    path('profile/update/<user_id>/', views.update_profile_page, name="update_profile_page"),
    path('my_posts/', views.added_company_list_view, name="added_company_list_view"),


]