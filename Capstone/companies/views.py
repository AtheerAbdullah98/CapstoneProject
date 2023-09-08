from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from .models import Company

# Create your views here.
def add_company_view(request: HttpRequest):
    try:
        msg= None
        # if not request.user.is_staff:
        #     return redirect("")

        if request.method == "POST":
            new_company = Company(name=request.POST["name"], field=request.POST["field"],info=request.POST["info"], description=request.POST["description"],image=request.FILES["image"])
            new_company.save()
            msg='Company added'

        return render(request, 'companies/add_company.html')
    except: 
        return redirect("main:home_view")
    

#updating company  
def company_update_view(request:HttpRequest, company_id):
    
   # if not request.user.is_staff:
    #    return redirect("accounts:login_user_view")
    
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

    return render(request, "companies/update_company.html")

#deleting company from database
def company_delete_view(request: HttpRequest, company):

    #if not request.user.is_staff:
        #return redirect("accounts:login_user_view")
    
    company = Company.objects.get(id=company)
    company.delete()

    return redirect("companies:all_companies_view")

def all_companies_view(request: HttpRequest):
    pass

def company_detail_view(request: HttpRequest):
    pass