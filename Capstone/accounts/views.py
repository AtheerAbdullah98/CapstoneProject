from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from .models import Profile
from companies.models import Company
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def register_user_view(request : HttpRequest):

    if request.method == "POST":
        new_user = User.objects.create_user(first_name=request.POST["first_name"], last_name=request.POST["last_name"], username=request.POST["username"], email=request.POST["email"], password=request.POST["password"], )
        new_user.save()
        profile=Profile.objects.create(user=new_user)
        profile.save()
        return redirect("accounts:login_user_view")
    

    return render(request, "accounts/register.html")


def login_user_view(request: HttpRequest):

    msg = None

    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])

        if user:
            login(request, user)
            return redirect("main:home_view")
        else:
            msg = "Username or password is no correct. No user found."


    return render(request, "accounts/login.html", {"msg": msg})



def logout_user_view(request: HttpRequest):

    logout(request)

    return redirect("accounts:login_user_view")

def profile_page(request:HttpRequest, user_id):

    try:
        profile = Profile.objects.get(user__id=user_id)
    except:
        return render(request, "main/not_found.html")

    return render(request, "accounts/profile.html", {"profile" : profile})

def update_profile_page(request:HttpRequest, user_id):

    try:
        user = User.objects.get(id=user_id)
        profile, is_created = Profile.objects.get_or_create(user=user)
    except:
        return render(request, "main/not_found.html")
    
    if request.method == "POST":
        profile.about = request.POST["about"]
        profile.twitter_link = request.POST["twitter_link"]
        profile.birth_date = request.POST["birth_date"]
        if "avatar" in request.FILES:
            profile.avatar = request.FILES["avatar"]
        profile.save()

        return redirect("accounts:profile_page", user_id=user_id)
        
    return render(request, "accounts/update_profile.html", {"profile" : profile})

def added_company_list_view(request,user_id ):
    companies = Company.objects.filter(id=user_id)


    return render(request, 'accounts/my_added_company.html', {'companies': companies})


