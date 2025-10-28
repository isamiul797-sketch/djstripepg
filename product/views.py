from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from product.models import Product,Order
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class ProductListView(View):
    def get(self,request):
        products = Product.objects.all()
        return render(request,'product/product_list.html',{'products':products})
    
class CheckoutView(LoginRequiredMixin,View):
    def get(self , request, product_id):
        product = get_object_or_404(Product,id = product_id)
        return render(request,'product/checkout.html',{'product':product})

def success(request):
    return JsonResponse({'status':'success'})

def cancel(request):
    return JsonResponse({'status':'cancel'})