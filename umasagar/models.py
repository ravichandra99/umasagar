from django.db import models
from authentication.models import MyUser,Company
import uuid

# Create your models here.

class CropGroup(models.Model):
	crop_group = models.CharField(max_length = 100)

	def __str__(self):
		return self.crop_group

class CropCode(models.Model):
	crop_code = models.CharField(max_length = 100)

	def __str__(self):
		return self.crop_code

class CropCategory(models.Model):
	crop_category = models.CharField(max_length = 100)

	def __str__(self):
		return self.crop_category

	class Meta:
		verbose_name = "Category"
		verbose_name_plural = "Categories"

class Stage(models.Model):
	stage = models.CharField(max_length = 100)

	def __str__(self):
		return self.stage

class VarietyCode(models.Model):
	variety_code = models.CharField(max_length = 100,unique = True,primary_key = True)

	def __str__(self):
		return self.variety_code

class UOM(models.Model):
	uom = models.CharField(max_length = 100)

	def __str__(self):
		return self.uom

class Product(models.Model):
	company = models.ForeignKey(Company, on_delete = models.CASCADE)
	crop_group = models.ForeignKey(CropGroup, on_delete = models.CASCADE)
	crop_code = models.ForeignKey(CropCode, on_delete = models.CASCADE)
	crop_category = models.ForeignKey(CropCategory, on_delete = models.CASCADE)
	stage = models.ForeignKey(Stage, on_delete = models.CASCADE)
	variety_code = models.OneToOneField(VarietyCode, on_delete = models.CASCADE,primary_key = True)
	uom = models.ForeignKey(UOM, on_delete = models.CASCADE)
	pack_size = models.CharField(max_length = 100)
	price = models.DecimalField(max_digits = 15,decimal_places = 2)

	def __str__(self):
		return str(self.variety_code)



class SaleBill(models.Model):
    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)
    dealer = models.ForeignKey(MyUser, on_delete = models.SET_NULL, related_name='saledealer',null = True,verbose_name = 'select user')
    name = models.CharField(max_length=150,blank = True,null = True)
    phone = models.CharField(max_length=13,blank = True,null = True)
    address = models.TextField()
    email = models.EmailField(max_length=254,blank = True,null = True)
    lrno = models.CharField(max_length = 254,blank = True,null = True,verbose_name = 'LR No.')
    vehicleno = models.CharField(max_length = 254,blank = True,null = True,verbose_name = 'Vehicle No.')
    #gstin = models.CharField(max_length=15)
    s1approve = models.BooleanField(default = False,verbose_name = 'Approve')
    s2approve = models.BooleanField(default = False,verbose_name = 'Approve')
    logapprove = models.BooleanField(default = False,verbose_name = 'Approve')


    def __str__(self):
        return "Bill no: " + str(self.billno)

    def get_items_list(self):
        return SaleItem.objects.filter(billno=self)

    def get_total_price(self):
        saleitems = SaleItem.objects.filter(billno=self)
        total = 0
        for item in saleitems:
            total += item.totalprice
        return total



#contains the sale stocks made
class SaleItem(models.Model):
    billno = models.ForeignKey(SaleBill, on_delete = models.CASCADE, related_name='salebillno')
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField(default=1)
    perprice = models.FloatField(default=1)
    totalprice = models.FloatField(default=1)

    def __str__(self):
	    return "Bill no: " + str(self.billno.billno) + ", Item = " + str(self.product.variety_code)



class SaleBillDetails(models.Model):
    billno = models.ForeignKey(SaleBill, on_delete = models.CASCADE, related_name='saledetailsbillno')
    
    eway = models.CharField(max_length=50, blank=True, null=True)    
    veh = models.CharField(max_length=50, blank=True, null=True)
    destination = models.TextField()
    po = models.CharField(max_length=50, blank=True, null=True)
    
    cgst = models.CharField(max_length=50, blank=True, null=True)
    sgst = models.CharField(max_length=50, blank=True, null=True)
    igst = models.CharField(max_length=50, blank=True, null=True)
    cess = models.CharField(max_length=50, blank=True, null=True)
    tcs = models.BooleanField(default = False)
    total = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
	    return "Bill no: " + str(self.billno.billno)