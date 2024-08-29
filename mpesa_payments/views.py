from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime
from datetime import datetime
from competition.models import MpesaTransaction
from .serializers import MpesaTransactionSerializer

@api_view(['POST'])
def mpesa_callback(request):
    data = request.data
    body = data.get("Body", {}).get("stkCallback", {})

    checkout_request_id = body.get("CheckoutRequestID")
    result_code = body.get("ResultCode")
    result_desc = body.get("ResultDesc")

    # Parse Mpesa callback data if transaction was successful
    if result_code == 0:  # 0 indicates success
        callback_metadata = body.get("CallbackMetadata", {}).get("Item", [])
        amount = next(item for item in callback_metadata if item["Name"] == "Amount")["Value"]
        mpesa_receipt_number = next(item for item in callback_metadata if item["Name"] == "MpesaReceiptNumber")["Value"]
        phone_number = next(item for item in callback_metadata if item["Name"] == "PhoneNumber")["Value"]
        transaction_date_str = next(item for item in callback_metadata if item["Name"] == "TransactionDate")["Value"]

        # Convert transaction_date to ISO 8601 format
        try:
            transaction_date = datetime.strptime(str(transaction_date_str), "%Y%m%d%H%M%S")
        except ValueError:
            return Response({"error": "Invalid transaction date format"}, status=status.HTTP_400_BAD_REQUEST)

        # Update or create the transaction in the database
        MpesaTransaction.objects.update_or_create(
            checkout_request_id=checkout_request_id,
            defaults={
                "result_code": result_code,
                "result_desc": result_desc,
                "amount": amount,
                "mpesa_receipt_number": mpesa_receipt_number,
                "transaction_date": transaction_date,
                "phone_number": phone_number,
                "user" : request.user,
            }
        )

        return Response({"status": "Payment received successfully"}, status=status.HTTP_200_OK)

    # Transaction failed
    else:
        MpesaTransaction.objects.update_or_create(
            checkout_request_id=checkout_request_id,
            defaults={
                "result_code": result_code,
                "result_desc": result_desc,
                "amount": 0,
                "mpesa_receipt_number": "N/A",
                "transaction_date": None,
                "phone_number": None,
            }
        )

        return Response({"status": "Payment failed, please retry"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def retrieve_payments(request):
    transactions = MpesaTransaction.objects.all()
    serializer = MpesaTransactionSerializer(transactions, many=True)
    return Response(serializer.data)