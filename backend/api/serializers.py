from rest_framework import serializers
from .models import Member, Sacrament, Pledge, Payment
from django.contrib.auth.models import User

class MemberSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Member
        fields = '__all__'

class SacramentSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.full_name', read_only=True)
    
    class Meta:
        model = Sacrament
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class PledgeSerializer(serializers.ModelSerializer):
    total_paid = serializers.ReadOnlyField()
    balance = serializers.ReadOnlyField()
    member_name = serializers.CharField(source='member.full_name', read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Pledge
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']