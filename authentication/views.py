from django.shortcuts import render
from authentication.models import MyUser

# Create your views here.
from wagtail.contrib.modeladmin.views import EditView
from wagtail.wagtailadmin.edit_handlers import (
    ObjectList,
    FieldPanel,
    get_form_for_model,
)

from edit_handlers import ReadOnlyPanel


class MyModelEditView(EditView):
    def get_form_class(self):
        return get_form_for_model(
            MyUser,
            fields = '__all_' #['readable_field'],
        )

    def get_edit_handler_class(self):
        edit_handler = ObjectList([
            ReadOnlyPanel('password'),
            FieldPanel('email'),
        ])
        return edit_handler.bind_to_model(self.model)


