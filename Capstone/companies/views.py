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
    