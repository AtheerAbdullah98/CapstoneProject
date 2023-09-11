from django.contrib import admin
from .models import Company, Favorite, Report,Review

# Register your models here.


class CompanyAdmin(admin.ModelAdmin):

    list_display = ("name", "field", "info","approved")
    list_filter = ("info",)


class ReviewAdmin(admin.ModelAdmin):

    list_display = ("user", "company", "rating")
    list_filter = ("company","rating",)

admin.site.register(Review, ReviewAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Favorite)
admin.site.register(Report)