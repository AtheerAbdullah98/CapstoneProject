from django.shortcuts import render, redirect, resolve_url
from django.http import HttpRequest, HttpResponse

from django.contrib.auth.models import User

from .models import Company,Review


# Create your views here.
def add_company_view(request: HttpRequest):
    try:
        msg= None
        if not request.user.is_authenticated:  
             return redirect("main:home_view")

        if request.method == "POST":
            if request.user.is_staff:  
                new_company = Company(user=request.user,name=request.POST["name"], field=request.POST["field"],info=request.POST["info"], description=request.POST["description"],image=request.FILES["image"],approved=True)
                new_company.save()
                msg='Company added'
                url = resolve_url("companies:all_companies_view") + "?msg=" + msg
                return redirect(url)
            else:
                new_company = Company(user=request.user,name=request.POST["name"], field=request.POST["field"],info=request.POST["info"], description=request.POST["description"],image=request.FILES["image"])
                new_company.save()
                msg='Company request added'
                url = resolve_url("companies:all_companies_view") + "?msg=" + msg
                return redirect(url)

        return render(request, 'companies/add_company.html')
    except: 
        return redirect("main:home_view")

    
def approve_company_view(request: HttpRequest):
    try:
        msg = None
        if not request.user.is_authenticated:  
             return redirect("main:home_view")

        companies = Company.objects.filter(approved=False)
        return render(request, "companies/approved_company.html", {"companies" : companies })
    except: 
        return redirect("main:home_view")

 #posts from admin   
# def admin_approve_view(request, company_id):
#     if request.user.is_staff:
#         company = Company.objects.get(id=company_id)
#         company.approved = True
#         company.save()
#         return redirect('companies/service_request_success.html')
#     else:
#         return redirect("accounts:login_user_view")
    

#updating company  
def company_update_view(request:HttpRequest, company_id):
    
    if not request.user.is_staff:
      return redirect("accounts:login_user_view")
    
    try:
        company = Company.objects.get(id=company_id)

        if request.method == "POST":
            company.name = request.POST["name"]
            company.field = request.POST["field"]
            company.info = request.POST["info"]
            company.description = request.POST["description"]
            if "image" in request.FILES:
                company.image = request.FILES["image"]
            company.save()

            return redirect("companies:company_detail_view", company_id=company.id)
    except:
        return render(request, "main/not_found.html")

    return render(request, "companies/update_company.html", {"company": company})

#deleting company from database
def company_delete_view(request: HttpRequest, company_id):

    if not request.user.is_staff:
        return redirect("accounts:login_user_view")
    
    company = Company.objects.get(id=company_id)
    company.delete()
    

    return redirect("companies:all_companies_view")

def all_companies_view(request: HttpRequest):

    #companies = Company.objects.all()
    companies = Company.objects.filter(approved=True)
    
    return render(request, "companies/all_companies.html", {"companies" : companies})


def company_detail_view(request: HttpRequest, company_id):
     
  company = Company.objects.get(id=company_id)
  reviews = Review.objects.filter(company=company)
  #experience_choices= Review.experience
  if request.method == "POST":
        if not request.user.is_staff:
            return redirect("accounts:login_user_view")
        company.approved = request.POST["approved"]
        company.save()
        msg='company approved'
        return redirect("companies:all_companies_view")
  
  return render(request, "companies/company_detail.html", {"company" : company,"reviews" : reviews, "Review" : Review})#,"experience_choices":experience_choices})

def companies_search_view(request: HttpRequest):

    if "search" in request.GET:
        companies = Company.objects.filter(name__contains=request.GET["search"])
    else:
        companies = Company.objects.all()

    return render(request, 'companies/search_results.html', {"companies" : companies})

#### Review views 
def add_Review_view(request: HttpRequest,company_id):

    company = Company.objects.get(id=company_id)

    if request.method == "POST" and request.user.is_authenticated:
        new_review = Review(user=request.user,company= company,experience=request.POST["experience"], position=request.POST["position"], description=request.POST["description"], rating= request.POST["rating"])
        new_review.save()


        return redirect("companies:company_detail_view",company.id)

    return render(request, 'companies/add_reveiw.html', {"company":company,"review":Review })
