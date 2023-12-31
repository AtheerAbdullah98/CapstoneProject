from django.shortcuts import render, redirect, resolve_url
from django.http import HttpRequest, HttpResponse

from django.contrib.auth.models import User
from accounts.models import Profile

from .models import Company, Favorite, Report,Review
from django.db.models import Count

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
                msg='تم إضافة الشركة'
                url = resolve_url("companies:all_companies_view") + "?msg=" + msg
                return redirect(url)
            else:
                new_company = Company(user=request.user,name=request.POST["name"], field=request.POST["field"],info=request.POST["info"], description=request.POST["description"],image=request.FILES["image"])
                new_company.save()
                msg='تم طلب إضافة شركة'
                url = resolve_url("companies:all_companies_view") + "?msg=" + msg
                return redirect(url)

        return render(request, 'companies/add_company.html')
    except: 
        return redirect("main:not_found_view")

def dashbord_view(request: HttpRequest, user_id):
    try:
        profile = Profile.objects.get(user__id=user_id)
    except:
        return render(request, "main/not_found.html")


    return render(request, "companies/dashboard.html",{"profile" : profile})

def approve_company_view(request: HttpRequest):
    try:
        msg = None
        if not request.user.is_authenticated:  
             return redirect("main:home_view")

        companies = Company.objects.filter(approved=False)
        return render(request, "companies/approved_company.html", {"companies" : companies })
    except: 
        return redirect("main:not_found_view")


#updating company  
def company_update_view(request:HttpRequest, company_id):
    
    if not request.user.is_staff:
      return redirect("accounts:login_user_view")
    
    company = Company.objects.get(id=company_id)

    try:

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
        return redirect("main:not_found_view")

    return render(request,"companies/update_company.html",{"company":company})

#deleting company from database
def company_delete_view(request: HttpRequest, company_id):
    try:

        if not request.user.is_staff:
            return redirect("accounts:login_user_view")
        
        company = Company.objects.get(id=company_id)
        company.delete()
        

        return redirect("companies:all_companies_view")
    except:
        return redirect("main:not_found_view")

def all_companies_view(request: HttpRequest):

    #companies = Company.objects.all()
    companies = Company.objects.filter(approved=True)
    
    return render(request, "companies/all_companies.html", {"companies" : companies})


def company_detail_view(request: HttpRequest, company_id):
    try:     
        company = Company.objects.get(id=company_id)
        reviews = Review.objects.filter(company=company)  
        # filter reviews
        for index, review in enumerate(reviews):
                reviews[index].is_favored = Favorite.objects.filter(user=request.user, review=review).exists()
        if "experience" and "position" in request.GET:
                experience = request.GET.get("experience")
                position= request.GET.get("position")
                order= request.GET.get("order")
                if experience !="all" and position != "all":
                    if order != "all":
                        Review.objects.filter(company=company,experience=experience,position=position).order_by(f"-{order}")
                        for index, review in enumerate(reviews):
                            reviews[index].is_favored = Favorite.objects.filter(user=request.user, review=review).exists()
                    if order == "favorite": 
                        reviews_favorite = Review.objects.filter(company=company,experience=experience,position=position).annotate(favorite_count=Count('favorite'))
                        reviews = reviews_favorite.order_by('-favorite_count')
                        for index, review in enumerate(reviews):
                            reviews[index].is_favored = Favorite.objects.filter(user=request.user, review=review).exists()
                        return render(request, "companies/company_detail.html", {"company" : company,"reviews" : reviews})
                    else:
                        reviews = Review.objects.filter(company=company,experience=experience,position=position)
                        for index, review in enumerate(reviews):
                            reviews[index].is_favored = Favorite.objects.filter(user=request.user, review=review).exists()
                    return render(request, "companies/company_detail.html", {"company" : company,"reviews" : reviews})
                if experience =="all" and position != "all":
                    if order != "all":
                        reviews = Review.objects.filter(company=company,position=position).order_by(f"-{order}")
                        for index, review in enumerate(reviews):
                            reviews[index].is_favored = Favorite.objects.filter(user=request.user, review=review).exists()
                    if order == "favorite": 
                        reviews_favorite = Review.objects.filter(company=company,position=position).annotate(favorite_count=Count('favorite'))
                        reviews = reviews_favorite.order_by('-favorite_count')
                        for index, review in enumerate(reviews):
                            reviews[index].is_favored = Favorite.objects.filter(user=request.user, review=review).exists()
                        return render(request, "companies/company_detail.html", {"company" : company,"reviews" : reviews})
                    else:
                        reviews = Review.objects.filter(company=company,position=position)
                        for index, review in enumerate(reviews):
                            reviews[index].is_favored = Favorite.objects.filter(user=request.user, review=review).exists()
                    return render(request, "companies/company_detail.html", {"company" : company,"reviews" : reviews})
                if experience !="all" and position == "all":
                    if order != "all":
                        reviews = Review.objects.filter(company=company,experience=experience).order_by(f"-{order}")
                        for index, review in enumerate(reviews):
                            reviews[index].is_favored = Favorite.objects.filter(user=request.user, review=review).exists()
                    if order == "favorite": 
                        reviews_favorite = Review.objects.filter(company=company,experience=experience).annotate(favorite_count=Count('favorite'))
                        reviews = reviews_favorite.order_by('-favorite_count')
                        for index, review in enumerate(reviews):
                            reviews[index].is_favored = Favorite.objects.filter(user=request.user, review=review).exists()
                        return render(request, "companies/company_detail.html", {"company" : company,"reviews" : reviews})
                    else:
                        reviews = Review.objects.filter(company=company,experience=experience)
                        for index, review in enumerate(reviews):
                            reviews[index].is_favored = Favorite.objects.filter(user=request.user, review=review).exists()
                    return render(request, "companies/company_detail.html", {"company" : company,"reviews" : reviews})
                else:
                    if order != "all":
                        reviews = Review.objects.filter(company=company).order_by(f"-{order}")
                        for index, review in enumerate(reviews):
                            reviews[index].is_favored = Favorite.objects.filter(user=request.user, review=review).exists()
                        return render(request, "companies/company_detail.html", {"company" : company,"reviews" : reviews})
                    if order == "favorite":
                        reviews_favorite = Review.objects.annotate(favorite_count=Count('favorite'))
                        reviews = reviews_favorite.order_by('-favorite_count')
                        for index, review in enumerate(reviews):
                            reviews[index].is_favored = Favorite.objects.filter(user=request.user, review=review).exists()
                        return render(request, "companies/company_detail.html", {"company" : company,"reviews" : reviews})
        # end filter reviews
        if request.method == "POST":
                if not request.user.is_staff:
                    return redirect("accounts:login_user_view")
                company.approved = request.POST["approved"]
                company.save()
                msg='تم الإضافة'
                return redirect("companies:all_companies_view")
        
        return render(request, "companies/company_detail.html", {"company" : company,"reviews" : reviews})
    except:
        return redirect("main:not_found_view")

def companies_search_view(request: HttpRequest):

    if "search" in request.GET:
        companies = Company.objects.filter(name__contains=request.GET["search"])
    elif "تقنية" in request.GET:
        companies = Company.objects.filter(field = "تقنية")
    elif "صحي" in request.GET:
        companies = Company.objects.filter(field = "صحي")
    elif "البنوك" in request.GET:
        companies = Company.objects.filter(field = "البنوك")
    elif "الاتصالات" in request.GET:
        companies = Company.objects.filter(field = "الاتصالات")
    else:
        companies = Company.objects.all()

    return render(request, 'companies/search_results.html', {"companies" : companies})

#### Review views 

def add_Review_view(request: HttpRequest,company_id):
    try:
        company = Company.objects.get(id=company_id)

        if request.method == "POST" and request.user.is_authenticated:
            new_review = Review(user=request.user,company= company,experience=request.POST["experience"], position=request.POST["position"], description=request.POST["description"], rating= request.POST["rating"])
            new_review.save()


            return redirect("companies:company_detail_view",company.id)

        return render(request, 'companies/add_reveiw.html', {"company":company,"review":Review })
    except:
        return redirect("main:not_found_view")


def review_delete_view(request: HttpRequest, review_id):
    try:
        review=Review.objects.get(id=review_id)
        if review.user ==request.user or request.user.is_staff:
            review.delete()
            return redirect('companies:company_detail_view',review.company.id)
        else:
            return redirect("accounts:login_user_view")
    except:
        return redirect("main:not_found_view")
    

def review_update_view(request:HttpRequest, review_id):
    try:
        is_user = Review.objects.get(id=review_id)
        if request.user.id != is_user.user.id and not request.user.is_staff:
            return redirect("accounts:login_user_view")
    
    
        review = Review.objects.get(id=review_id,)
        # companyId=Review.company.id
        if request.method == "POST":
            if "id" in request.GET:
                global company_id 
                company_id = request.GET['id']
                print(company_id)
                
            review.experience = request.POST["experience"]
            review.position = request.POST["position"]
            review.description = request.POST["description"]
            review.rating = request.POST["rating"]
            review.save()
            return redirect("companies:company_detail_view", company_id= company_id)
        return render(request,"companies/update_review.html",{"review":review })
    except:
        return redirect("main:not_found_view")

def all_reveiws_view(request: HttpRequest):
   
    # reveiws = Review.objects.filter( id= user_id )
    return render(request, "companies/all_reveiws.html")

def add_favorite_view(request: HttpRequest, review_id):

    try:
        if not request.user.is_authenticated:
            return redirect("accounts:login_user_view")
        url= request.META.get('HTTP_REFERER') 
        review = Review.objects.get(id=review_id)
        company_id= review.company.id

        if not Favorite.objects.filter(user=request.user, review=review).exists():
            new_favorite = Favorite(user=request.user, review=review)
            new_favorite.save()


        # return redirect("companies:company_detail_view", company_id= company_id)
        return redirect(url)
    except:
        return redirect("main:not_found_view")

def remove_favorite_view(request: HttpRequest, review_id):
    try:
        if not request.user.is_authenticated:
            return redirect("accounts:login_user_view")
        
        url= request.META.get('HTTP_REFERER')
        review = Review.objects.get(id=review_id)
        company_id= review.company.id
        user_favorite = Favorite.objects.filter(user=request.user, review=review).first()

        if user_favorite:
            user_favorite.delete()
            

        # return redirect("companies:company_detail_view", company_id= company_id)
        return redirect(url)
    except:
        return redirect("main:not_found_view")

def user_favorite_view(request: HttpRequest):
    return render(request,"companies/user_favorite.html")

def report_view(request: HttpRequest, review_id):
    try:

        if not request.user.is_authenticated:
            return redirect("accounts:login_user_view")
        
        
        review = Review.objects.get(id=review_id)
        company_id= review.company.id
        if Report.objects.filter(user=request.user, review=review).exists():
            msg='تم الإبلاغ مسبقاٌ'
            url = resolve_url("companies:company_detail_view" ,company_id) + "?msg=" + msg
            return redirect(url)
        if not Report.objects.filter(user=request.user, review=review).exists():
            new_report = Report(user=request.user, review=review)
            new_report.save()
            msg='تم الإبلاغ'
            url = resolve_url("companies:company_detail_view" ,company_id) + "?msg=" + msg
            return redirect(url)
        return redirect("companies:company_detail_view", company_id= company_id) 
    except:
        return redirect("main:not_found_view")

def all_report_view(request: HttpRequest):

    reports = Report.objects.all
    
    return render(request, "companies/all_report.html", {"reports" : reports})


def company_filter_view(request: HttpRequest):
# جزء تابع للهوم بيج يحذف بعدين
    
    
    return render(request, "companies/company_filter.html")

# def review_filter_view(request: HttpRequest,company_id):

#     if "search" in request.GET:
#         reviews = Review.objects.filter(name__contains=request.GET["search"])
#     elif "تقنية" in request.GET:
#         companies = Company.objects.filter(field = "تقنية")
#     elif "صحي" in request.GET:
#         companies = Company.objects.filter(field = "صحي")
#     elif "البنوك" in request.GET:
#         companies = Company.objects.filter(field = "البنوك")
#     elif "الاتصالات" in request.GET:
#         companies = Company.objects.filter(field = "الاتصالات")
#     else:
#         companies = Company.objects.all()

#     return render(request, 'companies/search_results.html', {"reviews" : reviews})