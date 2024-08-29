from django.urls import path
from .views import mpesa_callback, retrieve_payments

urlpatterns = [
    path('add-payment/', mpesa_callback, name='mpesa-callback'),
    path('payments/', retrieve_payments, name='retrieve-payments'),
]