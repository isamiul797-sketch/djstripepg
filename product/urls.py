from django.urls import path
from product.views import ProductListView, CheckoutView, success, cancel
urlpatterns = [
    path('',ProductListView.as_view(),name='product_list'),
    path('checkout/<int:product_id>',CheckoutView.as_view(),name='checkout'),
    path('success/',success,name='success'),
    path('cancel/',cancel,name='cancel'),
]
