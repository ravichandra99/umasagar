from wagtail.contrib.modeladmin.options import (
    ModelAdmin,ModelAdminGroup,modeladmin_register
)
from wagtail.admin.forms import WagtailAdminModelForm
from wagtail.admin import edit_handlers as panels

from authentication.models import MyUser,Zone,State,Region,Division,District,Mandal,Village
from django import forms


class MyWagtailForm(WagtailAdminModelForm):
    username = forms.CharField(disabled=True)
    first_name = forms.CharField(disabled=True)
    last_name = forms.CharField(disabled=True)


class MyUserAdmin(ModelAdmin):
    model = MyUser
    menu_label = 'My Users'
    menu_icon = 'pilcrow'
    add_to_settings_menu = True
    list_display = ('email', 'first_name', 'last_name')
    list_filter = ('usertype',)
    edit_handler = panels.TabbedInterface([
            panels.ObjectList([
                panels.FieldPanel("username"),
                panels.FieldPanel("first_name"),
                panels.FieldPanel("last_name"),
            ])
    ])

    edit_handler.base_form_class = MyWagtailForm


class ZoneAdmin(ModelAdmin):
    model = Zone
    menu_icon = 'pilcrow'  # change as required
    list_display = ('zone',)
    list_filter = ('zone',)
    search_fields = ('zone',)

class StateAdmin(ModelAdmin):
    model = State
    menu_icon = 'pilcrow'  # change as required
    list_display = ('state',)
    list_filter = ('state',)
    search_fields = ('state',)

class RegionAdmin(ModelAdmin):
    model = Region
    menu_icon = 'pilcrow'  # change as required
    list_display = ('region',)
    list_filter = ('region',)
    search_fields = ('region',)

class DivisionAdmin(ModelAdmin):
    model = Division
    menu_icon = 'pilcrow'  # change as required
    list_display = ('division',)
    list_filter = ('division',)
    search_fields = ('division',)

class DistrictAdmin(ModelAdmin):
    model = District
    menu_icon = 'pilcrow'  # change as required
    list_display = ('district',)
    list_filter = ('district',)
    search_fields = ('district',)

class MandalAdmin(ModelAdmin):
    model = Mandal
    menu_icon = 'pilcrow'  # change as required
    list_display = ('mandal',)
    list_filter = ('mandal',)
    search_fields = ('mandal',)

class VillageAdmin(ModelAdmin):
    model = Village
    menu_icon = 'pilcrow'  # change as required
    list_display = ('Village',)
    list_filter = ('village',)
    search_fields = ('village',)


class PlaceGroup(ModelAdminGroup):
    menu_label = 'Places'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 300  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (ZoneAdmin,StateAdmin,RegionAdmin,DivisionAdmin,DistrictAdmin,MandalAdmin,VillageAdmin)


modeladmin_register(MyUserAdmin)
modeladmin_register(PlaceGroup)


