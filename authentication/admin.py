from django.contrib import admin

# Register your models here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin
from authentication.models import MyUser,UserType,Company

class MyUserAdmin(UserAdmin):
    add_form = UserCreationForm
    
    #exclude = ('username',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),

        ('Personal info', {'fields': ('company','usertype','address','mobile')}),
        ('Permissions', {'fields': ('is_staff','groups')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email','first_name', 'last_name', 'password1', 'password2','usertype','company','address','mobile'),
        }),
    )

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(UserType)
admin.site.register(Company)
