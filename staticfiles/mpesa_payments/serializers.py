from rest_framework import serializers
from competition.models import MpesaTransaction

class MpesaTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaTransaction
        fields = '__all__'
