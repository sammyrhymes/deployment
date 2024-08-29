from django.shortcuts import render

# Create your views here.

def cart_summary(request):
    return render(request,'cart_summary.html')

def add_to_cart(request):
    return render(request,'add_to_cart.html')