from django.shortcuts import render, redirect, get_object_or_404

from .forms import CreateUserForm, LoginForm

from django.contrib.auth.decorators import login_required
from .models import *


# Authentication models and functions
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout


import json

from requests.auth import HTTPBasicAuth

from django.http import HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt

from competition.credentials import LipanaMpesaPpassword, MpesaAccessToken, MpesaC2bCredential

import requests

from datetime import datetime
import time
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, CreateUserForm

import base64
import sys



def user_auth(request):
    # Initialize both forms
    login_form = LoginForm()
    register_form = CreateUserForm()

    if request.method == 'POST':
        # Check which form is submitted by looking at the form name
        if 'login_submit' in request.POST:

            login_form = LoginForm(request, data=request.POST)

            if login_form.is_valid():

                username = request.POST.get('username')
                password = request.POST.get('password')

                user = authenticate(request, username=username, password=password)

                if user is not None:
                            
                    login(request, user)
                    next_url = request.GET.get('next')

                    print(next_url)
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect('/')
                else:
                    return render(request, 'cars_competition/log.html', {'error': 'Invalid credentials'})

        elif 'register_submit' in request.POST:


            if request.method == 'POST':

                register_form = CreateUserForm(request.POST)

                if register_form.is_valid():

                    register_form.save()

                    return redirect("login-user")

    context = {
        'loginform': login_form,
        'registerform': register_form,
    }
    return render(request, 'cars_competition/log.html', context)





# Create your views here.

def index(request):
    competitions = Competition.objects.all().order_by('-start_date')[:4]
    context = {
        'competitions': competitions,
    }
    return render(request, 'cars_competition/index.html', context)


@login_required
def dashboard(request):
    return render(request, 'cars_competition/dashboard.html')


def login_user(request):

    form = LoginForm()

    if request.method == 'POST':
        # Check which form is submitted by looking at the form name
        if 'login_submit' in request.POST:

            login_form = LoginForm(request, data=request.POST)

            if login_form.is_valid():

                username = request.POST.get('username')
                password = request.POST.get('password')

                user = authenticate(request, username=username, password=password)

            if user is not None:
                 
                next_url = request.GET.get('next')
                print(next_url)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('default_url') 
    

    context = {
        'loginform': form,
    }

    return render(request, 'cars_competition/login.html', context=context)


def logout_user(request):

    auth.logout(request)

    return redirect("dashboard")


# def register_user(request):

#     form = CreateUserForm()

#     if request.method == 'POST':

#         form = CreateUserForm(request.POST)

#         if register_form.is_valid():

#                     register_form.save()

#                     return redirect("login-user")

#     context = {
#         'registerform':form
#     }

#     return render(request, 'cars_competition/login.html', context=context)

def competitions(request):
    competitions = Competition.objects.all()
    return render(request, 'cars_competition/competitions.html', {'competitions': competitions})

def competition_details(request, competition_id):
    ticket_options = range(2, 21, 2) 
    competition = get_object_or_404(Competition, id=competition_id)
    images = CompetitionImage.objects.filter(competition=competition)
    return render(request, 'cars_competition/competition_details.html', {
        'competition': competition,
        'images': images,
        'ticket_options': ticket_options
    })


# def competition_details(request, competition_id):
#     competition = get_object_or_404(Competition, id=competition_id)
#     return render(request, 'cars_competition/competition_details.html', {'competition': competition})

@login_required(login_url="user_auth")
def add_to_basket(request, id):
    competition = get_object_or_404(Competition, id=id)
    if request.method == 'POST':
        ticket_count = int(request.POST['ticket_count'])
        print('first if')
        if ticket_count > 0 and ticket_count <= (competition.total_tickets - competition.tickets_sold):
            basket_item, created = BasketItem.objects.get_or_create(
                user=request.user,
                competition=competition,
                defaults={'ticket_count': ticket_count}
            )
            print('2 if')

            if not created:
                basket_item.ticket_count += ticket_count
                basket_item.save()
                print('3rd if')
            return redirect('competition', competition_id=competition.id)

    return redirect('competition', competition_id=competition.id)

@login_required(login_url="user_auth")
def view_basket(request):
    basket_items = BasketItem.objects.filter(user=request.user)
    total_cost = sum(item.competition.ticket_price * item.ticket_count for item in basket_items)
    return render(request, 'cars_competition/view_basket.html', {'basket_items': basket_items, 'total_cost': total_cost})

def remove_from_basket(request, item_id):
    item = get_object_or_404(BasketItem, id=item_id)
    item.delete()
    # Optionally add a success message or other logic
    return redirect('view_basket')  # Redirect to the basket view


def token(request):
    consumer_key = 'aWrsHLr8OiGyUlh2SjNVOalHxLOzAJGt'
    consumer_secret = 'my1Ofjv8W34lyVQx'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'upload_image.html', {"token":validated_mpesa_access_token})


def check_out(request):
    basket_items = BasketItem.objects.filter(user=request.user)
    total_cost = sum(item.competition.ticket_price * item.ticket_count for item in basket_items)
    return render(request, 'cars_competition/check_out.html', {'basket_items': basket_items, 'Amount': total_cost})


def stk(request):
    basket_items = BasketItem.objects.filter(user=request.user)
    total_cost = str(round(sum(item.competition.ticket_price * item.ticket_count for item in basket_items)))

    if request.method == "POST":
        phone = request.POST['phone']
        amount = total_cost
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request_data = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            # "CallBackURL": "https://django-daraja.vercel.app/",  # Replace with your actual callback URL
            "CallBackURL": "https://django-daraja.vercel.app/add-payment",
            # "CallBackURL": "https://127.0.0.1:8000",
            "AccountReference": "Dream Car",
            "TransactionDesc": "Web Development Charges"
        }
        
        response = requests.post(api_url, json=request_data, headers=headers)
        response_data = json.loads(response.text)

        print(response_data)
        check_out_request_id = response_data.get('CheckoutRequestID')

        if response_data.get('ResponseCode') == '0':
            # Simulate a delay for the user to complete the payment
            time.sleep(10)  

            # Fetch callback data
            callback_response = requests.get("https://django-daraja.vercel.app/payments/")
            callback_data = json.loads(callback_response.text)
            print(callback_data)

        

            # Process the callback data
            callback_data = callback_data.get('Body', {}).get('stkCallback', {})

            if callback_data.get('ResultCode') == 0:
                merchant_request_id = callback_data.get('MerchantRequestID')
                checkout_request_id = callback_data.get('CheckoutRequestID')
                result_code = callback_data.get('ResultCode')
                result_desc = callback_data.get('ResultDesc')

                metadata = callback_data.get('CallbackMetadata', {}).get('Item', [])
                amount = next(item for item in metadata if item['Name'] == 'Amount')['Value']
                mpesa_receipt_number = next(item for item in metadata if item['Name'] == 'MpesaReceiptNumber')['Value']
                transaction_date = next(item for item in metadata if item['Name'] == 'TransactionDate')['Value']
                phone_number = next(item for item in metadata if item['Name'] == 'PhoneNumber')['Value']

                # Convert transaction_date to a proper datetime object
                transaction_date = datetime.strptime(str(transaction_date), "%Y%m%d%H%M%S")

                # Save transaction to the database
                transaction = MpesaTransaction.objects.create(
                    user=request.user,  # Ensure the user is set correctly
                    merchant_request_id=merchant_request_id,
                    checkout_request_id=checkout_request_id,
                    result_code=result_code,
                    result_desc=result_desc,
                    amount=amount,
                    mpesa_receipt_number=mpesa_receipt_number,
                    transaction_date=transaction_date,
                    phone_number=phone_number,
                )
                transaction.save()

                # Payment processed successfully
                return redirect('payment_success')
            else:
                # Handle failure in callback response
                print("Payment failed:", callback_data.get('ResultDesc'))
                return redirect('payment_failure')

        else:
            # Payment request failed
            return redirect('check_out')

    return HttpResponse("Invalid request method.", status=405)
# def stk(request):

#     basket_items = BasketItem.objects.filter(user=request.user)
#     total_cost = str(round(sum(item.competition.ticket_price * item.ticket_count for item in basket_items)))

#     if request.method == "POST":
#         phone = request.POST['phone']
#         amount = total_cost
#         token = get_oauth_token()
#         password, timestamp = generate_password()

#         headers = {
#             "Authorization": f"Bearer {token}",
#             "Content-Type": "application/json"
#         }

#         payload = {
#             "BusinessShortCode": short_code,
#             "Password": password,
#             "Timestamp": timestamp,
#             "TransactionType": "CustomerPayBillOnline",
#             "Amount": amount,
#             "PartyA": phone,  # Phone number from user input
#             "PartyB": short_code,
#             "PhoneNumber": phone,  # Phone number from user input
#             "CallBackURL": callback_url,
#             "AccountReference": "Dream Car",
#             "TransactionDesc": "Web Development Charges"
#         }

#         response = requests.post(stk_push_url, headers=headers, json=payload)
#         response_data = response.json()

#         if response.status_code == 200:
#             check_out_request_id = response_data.get('CheckoutRequestID')

#             if response_data.get('ResponseCode') == '0':
#                 # Simulate a delay for the user to complete the payment
#                 time.sleep(10)  

#                 # Fetch callback data
#                 callback_response = requests.get(callback_url)
#                 callback_data = json.loads(callback_response.text)

#                 # Process the callback data
#                 callback_data = callback_data.get('Body', {}).get('stkCallback', {})

#                 if callback_data.get('ResultCode') == 0:
#                     merchant_request_id = callback_data.get('MerchantRequestID')
#                     checkout_request_id = callback_data.get('CheckoutRequestID')
#                     result_code = callback_data.get('ResultCode')
#                     result_desc = callback_data.get('ResultDesc')

#                     metadata = callback_data.get('CallbackMetadata', {}).get('Item', [])
#                     amount = next(item for item in metadata if item['Name'] == 'Amount')['Value']
#                     mpesa_receipt_number = next(item for item in metadata if item['Name'] == 'MpesaReceiptNumber')['Value']
#                     transaction_date = next(item for item in metadata if item['Name'] == 'TransactionDate')['Value']
#                     phone_number = next(item for item in metadata if item['Name'] == 'PhoneNumber')['Value']

#                     # Convert transaction_date to a proper datetime object
#                     transaction_date = datetime.strptime(str(transaction_date), "%Y%m%d%H%M%S")

#                     # Save transaction to the database
#                     transaction = MpesaTransaction.objects.create(
#                         user=request.user,  # Ensure the user is set correctly
#                         merchant_request_id=merchant_request_id,
#                         checkout_request_id=checkout_request_id,
#                         result_code=result_code,
#                         result_desc=result_desc,
#                         amount=amount,
#                         mpesa_receipt_number=mpesa_receipt_number,
#                         transaction_date=transaction_date,
#                         phone_number=phone_number,
#                     )
#                     transaction.save()

#                     # Payment processed successfully
#                     return redirect('payment_success')
#                 else:
#                     # Handle failure in callback response
#                     print("Payment failed:", callback_data.get('ResultDesc'))
#                     return redirect('payment_failure')

#             else:
#                 # Payment request failed
#                 print("Payment request failed:", response_data.get('ResponseDescription'))
#                 return redirect('check_out')

#         else:
#             # Failed to initiate STK Push
#             print("Failed to initiate STK Push")
#             print(response_data)
#             return redirect('check_out')

#     return HttpResponse("Invalid request method.", status=405)


def payment_success(request):
    # Display a success message to the user
    return render(request, 'cars_competition/payment_success.html')

def payment_failure(request):
    # Display a failure message to the user
    return render(request, 'cars_competition/payment_failure.html')
    
    
def base(request):
    return render(request, 'cars_competition/base.html', context={})

def portfolio(request):
    return render(request, 'cars_competition/portfolio-details.html', context={})

def service(request):
    return render(request, 'cars_competition/service-details.html', context={})

def starter(request):
    return render(request, 'cars_competition/starter-page.html', context={})