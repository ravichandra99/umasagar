from django.shortcuts import render,redirect, get_object_or_404, reverse
from django.http import HttpResponse,JsonResponse
from django.views.generic import (
    View, 
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.forms.models import inlineformset_factory
from umasagar.models import Product,SaleBillDetails,SaleBill,SaleItem
from authentication.models import MyUser
from umasagar.forms import SaleItemFormset,SelectDealerForm,SaleForm,\
Boss1ApproveForm,Boss2ApproveForm,LogApproveForm,SaleItemForm,dSaleItemForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from datetime import datetime
from django.db.models import Sum

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
        data = {'name':supplierobj.username,'phone':supplierobj.mobile,'email':supplierobj.email }
        form = SaleForm(data)
        
            
        if form.is_valid() and formset.is_valid():
            # saves bill
            billobj = form.save(commit=False)
            billobj.dealer = supplierobj
            billobj.user = request.user
            billobj.address = request.user.address
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
            saleitems = SaleItem.objects.filter(billno = salebill)
            for i in saleitems:
                i.despatched = i.quantity
                i.save()
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
        pk = kwargs['pk']
        sale = SaleBill.objects.get(pk = pk,s1approve = True,s2approve = True)
        form = self.form_class
        salebill = SaleBill.objects.get(billno = pk)
        supplierobj = get_object_or_404(MyUser, pk=salebill.dealer)
        no = SaleItem.objects.filter(billno=pk).count()
        SaleItemFormSet = inlineformset_factory(SaleBill, SaleItem, form=dSaleItemForm, fields=('quantity','despatched','remaining', 'perprice', 'product'),extra = no//2 - 1 if no//2 > 1 else 0)
        formset = SaleItemFormSet(instance=salebill)

        return render(request, self.template_name, {'form': form,'sale':sale,'formset':formset,'supplier':supplierobj})

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        salebill = SaleBill.objects.get(billno = pk)
        no = SaleItem.objects.filter(billno=pk).count()
        SaleItemFormSet = inlineformset_factory(SaleBill, SaleItem, form=dSaleItemForm, fields=('quantity','despatched','remaining', 'perprice', 'product'),extra = no//2 - 1 if no//2 > 1 else 0)
        formset = SaleItemFormSet(request.POST, instance=salebill)
        
        supplierobj = salebill.dealer
        #                       # gets the supplier object
        data = {'name':supplierobj.username,'phone':supplierobj.mobile,'email':supplierobj.email }
        saleform = SaleForm(data)
        
            
        if saleform.is_valid() and formset.is_valid():
            # saves bill
            billobj = saleform.save(commit=False)
            billobj.dealer = supplierobj
            billobj.user = request.user
            billobj.address = request.user.address
            billobj.order = salebill.order
            billobj.s1approve = True
            billobj.s2approve = True
            billobj.save()     
            # create bill details object
            billdetailsobj = SaleBillDetails(billno=billobj)
            billdetailsobj.save()
            old,new = pk,billobj.billno
            print(old,new)
            for f in formset:                                  # for loop to save each individual form as its own object
                
                billitem = f.save(commit = False)
                billitem.billno = SaleBill.objects.get(billno = new)
                billitem.totalprice = billitem.remaining * billitem.perprice 
                print(billitem.billno,billitem.product,billitem.quantity,billitem.remaining,billitem.despatched)
                billitem.save()

            for g in formset:

                saleitem = SaleItem(billno = salebill)
                saleitem.product = g.cleaned_data['product']
                saleitem.quantity = g.cleaned_data['quantity']
                remaining = g.cleaned_data['remaining']
                # despatched = g.cleaned_data['despatched']
                saleitem.perprice = g.cleaned_data['perprice']
                # saleitem.remaining,saleitem.despatched = saleitem.despatched,saleitem.remaining
                total_remaining = SaleItem.objects.filter(billno__order = salebill.order).filter(product = saleitem.product).aggregate(Sum('remaining'))['remaining__sum']
                total_despatched = SaleItem.objects.filter(billno__order = salebill.order).filter(product = saleitem.product).aggregate(Sum('despatched'))['despatched__sum']
                print(total_remaining,total_despatched)
                saleitem.remaining = total_remaining
                saleitem.despatched = saleitem.quantity - saleitem.remaining
                salebill.logapprove = False
                print(saleitem.billno,saleitem.product,saleitem.quantity,saleitem.remaining,saleitem.despatched)
                saleitem.save()
                salebill.save()


        form = self.form_class(request.POST)
        if form.is_valid():
            approve = request.POST.get("logapprove")
            lrno = request.POST.get("lrno")
            vehicleno = request.POST.get("vehicleno")
            transporter = request.POST.get("transporter")
            result = True if approve == 'on' else False
            

            nsalebill = get_object_or_404(SaleBill, pk = billobj.billno)
            nsalebill.lrno = lrno
            nsalebill.vehicleno = vehicleno
            nsalebill.logapprove = result

            nsalebill.save()

            itembill = SaleItem.objects.filter(billno=billobj.billno)

            billdetails = SaleBillDetails.objects.get(billno=billobj.billno)

            total_amount = [round(i.totalprice ,2) for i in itembill]
            total = round(sum(total_amount),2)
            billdetails.destination = nsalebill.dealer.address

            billdetails.total = total
            print(billdetails.total,'...total')
            billdetails.igst = datetime.today()
            billdetails.veh = nsalebill.vehicleno
            billdetails.po = nsalebill.lrno
            billdetails.user = request.user
            billdetails.transporter = transporter
            billdetails.tcs = True
            billdetails.save()
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
        try:
        
            if self.request.user.usertype.usertype == 'user':
                context = {'bills': SaleBill.objects.filter(dealer = self.request.user)}
            elif self.request.user.usertype.usertype == 'logistics':
                self.template_name = 'despatch_list.html'
                orders_list = list(dict.fromkeys([i.order for i in SaleBill.objects.all()]))
                context = {'bills': [SaleBill.objects.filter(order = i) for i in orders_list],'bill':SaleBillDetails.objects.all()}
            elif self.request.user.usertype.usertype == 'salesrep':
                context = {'bills': SaleBill.objects.filter(user = self.request.user)}
            else:
                pass

        except:
            context = {'bills' : None }

        return context

    # def get_context_data(self, *args, **kwargs):
    #     context = super(SaleView, self).get_context_data(*args, **kwargs)
    #     orders_list = list(dict.fromkeys([i.order for i in SaleBill.objects.all()]))
    #     print(orders_list)
    #     context['bills'] = [SaleBill.objects.filter(order = i) for i in orders_list]
    #     return context

def getprice(request):

    if request.is_ajax():
        product = request.GET.get('product')
        p = Product.objects.get(variety_code_id = product)
        price = p.price
        result = {'price':price}

    return JsonResponse(result)


# used to display the sale bill object
class SaleBillView(View):
    
    template_name = "sale_bill.html"

    
    def get(self, request, billno):
        bill = SaleBill.objects.get(billno=billno)
        items = SaleItem.objects.filter(billno=billno)
        billdetails = SaleBillDetails.objects.get(billno=billno)

        context = {
            'bill'          : bill,
            'items'         : items,
            'billdetails'   : billdetails,
        }
        return render(request, self.template_name, context)


def edit_sale(request ,name, billno):


    salebill = SaleBill.objects.get(billno = billno)
    no = SaleItem.objects.filter(billno=billno).count()
    SaleItemFormSet = inlineformset_factory(SaleBill, SaleItem, form=SaleItemForm, fields=('quantity', 'perprice', 'product'),extra = no//2 - 1 if no//2 > 1 else 0)

    formset = SaleItemFormSet(instance=salebill)


    if request.method == 'POST':  
        formset = SaleItemFormSet(request.POST, instance=salebill)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    billitem = form.save(commit=False)                                       # links the bill object to the items
                    
                    # calculates the total price
                    billitem.totalprice = billitem.perprice * billitem.quantity
                   
                    # saves bill item
                    try:
                        billitem.save()
                    except:
                        messages.info(request, 'Select any Product')
                        return redirect('umasagar:sales-list')

                    #form.save()

            messages.success(request, 'The Sale Bill {} is Updated.'.format(salebill.billno))
            return redirect('umasagar:sales-list')

    else:
        supplierobj = get_object_or_404(MyUser, pk=name)
        formset = SaleItemFormSet(instance=salebill)

    return render(request,'edit_sale.html',{'supplier':supplierobj, 'formset':formset})

    






