from django.contrib import admin
from .models import Company

# Register your models here.


class CompanyAdmin(admin.ModelAdmin):

    list_display = ("name", "field", "info")
    list_filter = ("info",)

admin.site.register(Company, CompanyAdmin)

