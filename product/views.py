from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from product.models import Product,Order
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

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


@method_decorator(csrf_exempt,name='dispatch')
class CreatePaymentView(LoginRequiredMixin, View):
    def post(self , request, product_id):
        product = get_object_or_404(Product, id=product_id)
        order = Order.objects.create(
            user=request.user,
            product=product,
            amount=product.price
        )

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data':{
                        'currency':'usd',
                        'unit_amount': int(product.price * 100),
                        'product_data':{
                            'name':product.name
                        }
                    },
                    "quantity":1,
                },],
            mode='payment',
            customer_email=request.user.email,
            success_url= 'http://localhost:8000/success/',
            cancel_url= 'http://localhost:8000//cancel/',
        )
        order.stripe_checkout_session_id = checkout_session.id
        order.save()
        return redirect(checkout_session.url)

@method_decorator(csrf_exempt,name='dispatch')
class StripeWebhookView(View):
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        try:
            event = stripe.Webhook.construct_event(payload,sig_header,endpoint_secret)
        except ValueError as e:
            return JsonResponse({'error':str(e)}, status=400)
        except stripe.error.SignatureVerificationError as e :
            return JsonResponse({'error':str(e)}, status=400)
        
        #Handle successfull payment
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            order = Order.objects.get(stripe_checkout_session_id=session['id'])
            order.is_paid = True
            order.save()
            return JsonResponse({'status':'success'})
        return JsonResponse({'status':'unhandled_event'})