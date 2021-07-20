from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from umasagar.models import (
    CropGroup,CropCode,CropCategory,Stage,VarietyCode,UOM,Product)
from authentication.models import Company

class CompanyAdmin(ModelAdmin):
    model = Company
    menu_icon = 'pilcrow'  # change as required
    list_display = ('company',)
    list_filter = ('company',)
    search_fields = ('company',)

class CropGroupAdmin(ModelAdmin):
    model = CropGroup
    menu_icon = 'pilcrow'  # change as required
    list_display = ('crop_group',)
    list_filter = ('crop_group',)
    search_fields = ('crop_group',)

class CropCodeAdmin(ModelAdmin):
    model = CropCode
    menu_icon = 'pilcrow'  # change as required
    list_display = ('crop_code',)
    list_filter = ('crop_code',)
    search_fields = ('crop_code',)

class CropCategoryAdmin(ModelAdmin):
    model = CropCategory
    menu_icon = 'pilcrow'  # change as required
    list_display = ('crop_category',)
    list_filter = ('crop_category',)
    search_fields = ('crop_category',)

class StageAdmin(ModelAdmin):
    model = Stage
    menu_icon = 'pilcrow'  # change as required
    list_display = ('stage',)
    list_filter = ('stage',)
    search_fields = ('stage',)

class VarietyCodeAdmin(ModelAdmin):
    model = VarietyCode
    menu_icon = 'pilcrow'  # change as required
    list_display = ('variety_code',)
    list_filter = ('variety_code',)
    search_fields = ('variety_code',)

class UOMAdmin(ModelAdmin):
    model = UOM
    menu_icon = 'pilcrow'  # change as required
    list_display = ('uom',)
    list_filter = ('uom',)
    search_fields = ('uom',)

class ProductAdmin(ModelAdmin):
    model = Product
    menu_icon = 'pilcrow'  # change as required
    list_display = ('variety_code','price')
    list_filter = ('variety_code',)
    search_fields = ('variety_code',)

class ProductGroup(ModelAdminGroup):
    menu_label = 'Products'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (CompanyAdmin, CropCategoryAdmin, CropGroupAdmin, CropCodeAdmin, StageAdmin, VarietyCodeAdmin, UOMAdmin, ProductAdmin)

# When using a ModelAdminGroup class to group several ModelAdmin classes together,
# you only need to register the ModelAdminGroup class with Wagtail:
modeladmin_register(ProductGroup)

