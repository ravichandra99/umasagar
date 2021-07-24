from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register
)
from wagtail.admin.forms import WagtailAdminModelForm
from wagtail.admin import edit_handlers as panels

from authentication.models import MyUser
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


modeladmin_register(MyUserAdmin)


