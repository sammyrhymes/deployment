from django.urls import path
from . import views
urlpatterns = [
   path('cart-summary',views.cart_summary, name= 'cart-summary'),
   path('add-to-cart',views.add_to_cart, name= 'add-to-cart'),
#    path('',views., name= ''),
#    path('',views., name= ''),
]