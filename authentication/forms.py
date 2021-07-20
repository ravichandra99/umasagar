from django import forms
from django.utils.translation import gettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm

from authentication.models import Zone,State,Region,Divison,District,Mandal,Village,UserType,Company,MyUser
from phonenumber_field.formfields import PhoneNumberField


class CustomUserEditForm(UserEditForm):
    zone = forms.ModelChoiceField(queryset=Zone.objects, required=False, label=_("Zone"))
    state = forms.ModelChoiceField(queryset=State.objects, required=False, label=_("State"))
    region = forms.ModelChoiceField(queryset=Region.objects, required=False, label=_("Region"))
    divison = forms.ModelChoiceField(queryset=Divison.objects, required=False, label=_("Division"))
    district = forms.ModelChoiceField(queryset=District.objects, required=False, label=_("District"))
    mandal = forms.ModelChoiceField(queryset=Mandal.objects, required=False, label=_("Mandal"))
    village = forms.ModelChoiceField(queryset=Village.objects, required=False, label=_("Village"))
    company = forms.ModelChoiceField(queryset=Company.objects, required=False, label=_("Company"))
    address = forms.CharField(widget=forms.Textarea,required = False,label = _("Address"))
    usertype = forms.ModelChoiceField(queryset=UserType.objects, required=True, label=_("User Type"))
    officer = forms.ModelChoiceField(queryset=MyUser.objects, required=False, label=_("Officer"))
    mobile = PhoneNumberField()


class CustomUserCreationForm(UserCreationForm):
    zone = forms.ModelChoiceField(queryset=Zone.objects, required=False, label=_("Zone"))
    state = forms.ModelChoiceField(queryset=State.objects, required=False, label=_("State"))
    region = forms.ModelChoiceField(queryset=Region.objects, required=False, label=_("Region"))
    divison = forms.ModelChoiceField(queryset=Divison.objects, required=False, label=_("Division"))
    district = forms.ModelChoiceField(queryset=District.objects, required=False, label=_("District"))
    mandal = forms.ModelChoiceField(queryset=Mandal.objects, required=False, label=_("Mandal"))
    village = forms.ModelChoiceField(queryset=Village.objects, required=False, label=_("Village"))
    company = forms.ModelChoiceField(queryset=Company.objects, required=False, label=_("Company"))
    address = forms.CharField(widget=forms.Textarea,required = False,label = _("Address"))
    usertype = forms.ModelChoiceField(queryset=UserType.objects, required=True, label=_("User Type"))
    officer = forms.ModelChoiceField(queryset=MyUser.objects, required=False, label=_("Officer"))
    mobile = PhoneNumberField()

