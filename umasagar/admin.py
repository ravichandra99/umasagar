from django.contrib import admin
from umasagar.models import SaleBillDetails,SaleItem,SaleBill

# Register your models here.

admin.site.register(SaleBillDetails)
admin.site.register(SaleBill)
admin.site.register(SaleItem)

