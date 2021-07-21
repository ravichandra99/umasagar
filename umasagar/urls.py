from django.urls import path
from umasagar.views import index,SelectSupplierView,PurchaseCreateView,Boss1ApproveView,\
Boss2ApproveView,SaleView,LogApproveView,getprice,SaleBillView

app_name = 'umasagar'

urlpatterns = [

    path('', index, name = 'index'),
    path('customer/new', SelectSupplierView.as_view(), name='select-supplier'),
    path('customer/new/<str:pk>', PurchaseCreateView.as_view(), name='new-purchase'),
    path('sales/', SaleView.as_view(), name='sales-list'),
    path('b1approve/<int:pk>',Boss1ApproveView.as_view(),name = 'b1-approve'),
    path('b2approve/<int:pk>',Boss2ApproveView.as_view(),name = 'b2-approve'),
    path('logapprove/<int:pk>',LogApproveView.as_view(),name = 'log-approve'),
    path('getprice/',getprice,name = 'getprice'),
    path('sales/<billno>', SaleBillView.as_view(), name="sale-bill"),

    
]