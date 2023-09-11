from django.shortcuts import render, redirect, resolve_url
from django.http import HttpRequest, HttpResponse

from django.contrib.auth.models import User

from .models import Company, Favorite,Review


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
  

  for index, review in enumerate(reviews):
      reviews[index].is_favored = Favorite.objects.filter(user=request.user, review=review).exists()
  
  #experience_choices= Review.experience
  if request.method == "POST":
        if not request.user.is_staff:
            return redirect("accounts:login_user_view")
        company.approved = request.POST["approved"]
        company.save()
        msg='company approved'
        return redirect("companies:all_companies_view")
  
  return render(request, "companies/company_detail.html", {"company" : company,"reviews" : reviews, "Review" : Review})

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


def review_delete_view(request: HttpRequest, review_id):
    is_user = Review.objects.get(id=review_id)
    if request.user.id != is_user.user.id and not request.user.is_staff:
            # print(request.user.id == is_user.user.id)
            return redirect("accounts:login_user_view")
    
    isreview = Review.objects.filter(user=request.user)
    review = Review.objects.get(id=review_id)
    review.delete()
    

    return redirect("companies:all_companies_view")

def review_update_view(request:HttpRequest, review_id):
    # try:
        is_user = Review.objects.get(id=review_id)
        if request.user.id != is_user.user.id and not request.user.is_staff:
            return redirect("accounts:login_user_view")
    
    
        review = Review.objects.get(id=review_id,)
        # companyId=Review.company.id

        if request.method == "POST":
            review.experience = request.POST["experience"]
            review.position = request.POST["position"]
            review.description = request.POST["description"]
            review.rating = request.POST["rating"]
            review.save()

            # return redirect("companies:company_detail_view", review_id=review.id)
        return render(request,"companies/update_review.html",{"review":review })
    # except:
    #     return render(request, "main/not_found.html")

    # return render(request, "companies/update_review.html",review.id)

def all_reveiws_view(request: HttpRequest):
    
   
    # reveiws = Review.objects.filter( id= user_id )
    return render(request, "companies/all_reveiws.html")

def add_favorite_view(request: HttpRequest, review_id):

    if not request.user.is_authenticated:
        return redirect("accounts:login_user_view")
    

    review = Review.objects.get(id=review_id)
    company_id= review.company.id
    print('test here')
    is_favorite = Favorite.objects.filter(user=request.user, review=review).exists()
    if not Favorite.objects.filter(user=request.user, review=review).exists():
        new_favorite = Favorite(user=request.user, review=review)
        print('test fav')
        new_favorite.save()
        print(new_favorite)
        print(request.user.favorite_set.all)

    return redirect("companies:company_detail_view", company_id= company_id)

def remove_favorite_view(request: HttpRequest, review_id):

    if not request.user.is_authenticated:
        return redirect("accounts:login_user_view")
    

    review = Review.objects.get(id=review_id)
    company_id= review.company.id
    user_favorite = Favorite.objects.filter(user=request.user, review=review).first()

    if user_favorite:
        user_favorite.delete()
        

    return redirect("companies:company_detail_view", company_id= company_id)