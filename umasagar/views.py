from django.shortcuts import render,redirect, get_object_or_404, reverse
from django.http import HttpResponse
from django.views.generic import (
    View, 
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)

from umasagar.models import Product,SaleBillDetails,SaleBill
from authentication.models import MyUser
from umasagar.forms import SaleItemFormset,SelectDealerForm,SaleForm,\
Boss1ApproveForm,Boss2ApproveForm,LogApproveForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.
def index(request):
	return render(request,'index.html')



# used to select the customer
class SelectSupplierView(LoginRequiredMixin,View):
    form_class = SelectDealerForm
    template_name = 'select_customer.html'

    def get(self, request, *args, **kwargs):                                    # loads the form page
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):                                   # gets selected supplier and redirects to 'PurchaseCreateView' class
        form = self.form_class(request.POST)
        print(form)
        print(request.POST)
        if form.is_valid():
            supplierid = request.POST.get("dealer")
            supplier = get_object_or_404(MyUser, username=supplierid)
            print(supplier.pk)
            return redirect('umasagar:new-purchase', supplier.pk)
        return render(request, self.template_name, {'form': form})


# used to generate a bill object and save items
class PurchaseCreateView(LoginRequiredMixin,View):                                                 
    template_name = 'new_sale.html'

    def get(self, request, pk):
        formset = SaleItemFormset(request.GET or None)                      # renders an empty formset
        supplierobj = get_object_or_404(MyUser, pk=pk)                        # gets the supplier object
        context = {
            'formset'   : formset,
            'supplier'  : supplierobj,
        }                                                                       # sends the supplier and formset as context
        return render(request, self.template_name, context)

    def post(self, request, pk):
        formset = SaleItemFormset(request.POST)                             # recieves a post method for the formset
        supplierobj = get_object_or_404(MyUser, pk=pk)
        #                       # gets the supplier object
        data = {'name':supplierobj.username,'phone':supplierobj.mobile,'email':supplierobj.email}
        form = SaleForm(data)
        
            
        if form.is_valid() and formset.is_valid():
            # saves bill
            billobj = form.save(commit=False)
            billobj.dealer = supplierobj
            billobj.save()     
            # create bill details object
            billdetailsobj = SaleBillDetails(billno=billobj)
            billdetailsobj.save()
            for form in formset:                                  # for loop to save each individual form as its own object
                print(form)
                # false saves the item and links bill to the item

                billitem = form.save(commit=False)
                billitem.billno = billobj                                       # links the bill object to the items
                    
                # calculates the total price
                billitem.totalprice = billitem.perprice * billitem.quantity
                   
                # saves bill item
                try:
                    billitem.save()
                except:
                    messages.info(request, 'Select any Product')
                    return redirect('umasagar:sales-list')

                if settings.USE_EMAIL:
                    #current_site = get_current_site(request)
                    send_mail(
    'Waiting for Approval !',
    "Hi, {} 's sale bill {} is waiting for your approval , Visit {} .".format(supplierobj,billobj,\
        request.build_absolute_uri(reverse('umasagar:b1-approve', kwargs={'pk':billobj.pk})) ),
    settings.DEFAULT_FROM_EMAIL,
    [request.user.officer.email,],
    fail_silently=False,
)
            messages.success(request, 'Approval is Sent Successfully.')
            
        return redirect('umasagar:sales-list')

class Boss1ApproveView(LoginRequiredMixin,View):
    form_class = Boss1ApproveForm
    template_name = 'b1_approve.html'

    def get(self, request, *args, **kwargs):                                    # loads the form page
        sale = SaleBill.objects.get(pk = kwargs['pk'])
        form = self.form_class
        return render(request, self.template_name, {'form': form,'sale':sale})

    def post(self, request, *args, **kwargs):                                   # gets selected supplier and redirects to 'PurchaseCreateView' class
        form = self.form_class(request.POST)
        if form.is_valid():
            approve = request.POST.get("s1approve")
            result = True if approve == 'on' else False
            salebill = get_object_or_404(SaleBill, pk = kwargs['pk'])
            salebill.s1approve = result
            salebill.save()
            if settings.USE_EMAIL and result:
                    #current_site = get_current_site(request)
                    send_mail(
    'Waiting for Approval !',
    "Hi, {} 's sale bill {} is waiting for your approval , Visit {} .".format(salebill.dealer,salebill.billno,\
        request.build_absolute_uri(reverse('umasagar:b2-approve', kwargs={'pk':salebill.pk})) ),
    settings.DEFAULT_FROM_EMAIL,
    [request.user.officer.email,],
    fail_silently=False,
)
                    messages.success(request, 'Approval is Sent Successfully.')
            return redirect('umasagar:sales-list')
        return render(request, self.template_name, {'form': form})

class Boss2ApproveView(LoginRequiredMixin,View):
    form_class = Boss2ApproveForm
    template_name = 'b2_approve.html'

    def get(self, request, *args, **kwargs):                                    # loads the form page
        sale = SaleBill.objects.get(pk = kwargs['pk'],s1approve = True)
        form = self.form_class
        return render(request, self.template_name, {'form': form,'sale':sale})

    def post(self, request, *args, **kwargs):                                   # gets selected supplier and redirects to 'PurchaseCreateView' class
        form = self.form_class(request.POST)
        if form.is_valid():
            approve = request.POST.get("s2approve")
            result = True if approve == 'on' else False
            salebill = get_object_or_404(SaleBill, pk = kwargs['pk'])
            salebill.s2approve = result
            salebill.save()
            if settings.USE_EMAIL and result:
                    #current_site = get_current_site(request)
                    send_mail(
    'Waiting for Approval !',
    "Hi, {} 's sale bill {} is waiting for your approval , Visit {} .".format(salebill.dealer,salebill.billno,\
        request.build_absolute_uri(reverse('umasagar:b2-approve', kwargs={'pk':salebill.pk})) ),
    settings.DEFAULT_FROM_EMAIL,
    [request.user.officer.email,],
    fail_silently=False,
)
                    messages.success(request, 'Approval is Sent Successfully.')
            return redirect('umasagar:sales-list')
        return render(request, self.template_name, {'form': form})


class LogApproveView(LoginRequiredMixin,View):
    form_class = LogApproveForm
    template_name = 'log_approve.html'

    def get(self, request, *args, **kwargs):                                    # loads the form page
        sale = SaleBill.objects.get(pk = kwargs['pk'],s1approve = True,s2approve = True)
        form = self.form_class
        return render(request, self.template_name, {'form': form,'sale':sale})

    def post(self, request, *args, **kwargs):                                   # gets selected supplier and redirects to 'PurchaseCreateView' class
        form = self.form_class(request.POST)
        if form.is_valid():
            approve = request.POST.get("logapprove")
            result = True if approve == 'on' else False
            salebill = get_object_or_404(SaleBill, pk = kwargs['pk'])
            salebill.logapprove = result
            salebill.save()
#             if settings.USE_EMAIL and result:
#                     #current_site = get_current_site(request)
#                     send_mail(
#     'Waiting for Approval !',
#     "Hi, {} 's sale bill {} is waiting for your approval , Visit {} .".format(salebill.dealer,salebill.billno,\
#         request.build_absolute_uri(reverse('umasagar:b2-approve', kwargs={'pk':salebill.pk})) ),
#     settings.DEFAULT_FROM_EMAIL,
#     [request.user.officer.email,],
#     fail_silently=False,
# )
            messages.success(request, 'The Sale Approved.')
            return redirect('umasagar:sales-list')
        return render(request, self.template_name, {'form': form})


# shows the list of bills of all sales 
class SaleView(LoginRequiredMixin,ListView):
    model = SaleBill
    template_name = "sales_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        # Call the base implementation first to get a context
        context = super(SaleView, self).get_context_data(*args, **kwargs)
        # add whatever to your context:
        
        if self.request.user.usertype.usertype == 'user':
            print(self.request.user)
            context = {'bills': SaleBill.objects.filter(dealer = self.request.user)}
        return context




