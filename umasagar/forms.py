from django import forms
from umasagar.models import SaleItem,Product,SaleBill
from authentication.models import MyUser
from django.forms import formset_factory


class SelectDealerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dealer'].queryset = MyUser.objects.filter(usertype__usertype = 'user')
        self.fields['dealer'].widget.attrs.update({'class': 'textinput form-control'})

    class Meta:
        model = SaleBill
        fields = ['dealer']

# form used for supplier
class SaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only'})
        self.fields['phone'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern' : '[0-9]{10}', 'title' : 'Numbers only'})
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control'})

    class Meta:
        model = SaleBill
        fields = ['name', 'phone', 'email', ]
        


# form used to get customer details
        

# form used to render a single stock item form
class SaleItemForm(forms.ModelForm):
    #product = forms.CharField(widget = forms.TextInput)
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()
        self.fields['product'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['perprice'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true'})

        

    class Meta:
        model = SaleItem
        fields = ['quantity', 'perprice', 'product']


# formset used to render multiple 'SaleItemForm'
SaleItemFormset = formset_factory(SaleItemForm, extra=1)


class Boss1ApproveForm(forms.ModelForm):

    class Meta:
        model = SaleBill
        fields = ['s1approve',]

class Boss2ApproveForm(forms.ModelForm):

    class Meta:
        model = SaleBill
        fields = ['s2approve',]

class LogApproveForm(forms.ModelForm):

    class Meta:
        model = SaleBill
        fields = ['lrno','vehicleno','logapprove',]


