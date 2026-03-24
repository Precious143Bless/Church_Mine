from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Member, Sacrament, Pledge, Payment
from .serializers import (
    MemberSerializer, SacramentSerializer, 
    PledgeSerializer, PaymentSerializer, UserSerializer
)

# Authentication Views
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })
    else:
        return Response({'error': 'Invalid credentials'}, 
                       status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({'message': 'Logged out successfully'})

# Member Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def members(request):
    if request.method == 'GET':
        search = request.GET.get('search', '')
        members = Member.objects.filter(is_active=True)
        
        if search:
            members = members.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(contact_number__icontains=search)
            )
        
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def member_detail(request, pk):
    try:
        member = Member.objects.get(pk=pk)
    except Member.DoesNotExist:
        return Response({'error': 'Member not found'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MemberSerializer(member)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = MemberSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        member.is_active = False
        member.save()
        return Response({'message': 'Member deactivated'})

# Sacrament Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def sacraments(request):
    if request.method == 'GET':
        sacrament_type = request.GET.get('type', '')
        member_id = request.GET.get('member', '')
        
        sacraments = Sacrament.objects.all()
        
        if sacrament_type:
            sacraments = sacraments.filter(sacrament_type=sacrament_type)
        if member_id:
            sacraments = sacraments.filter(member_id=member_id)
        
        serializer = SacramentSerializer(sacraments, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = SacramentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def sacrament_detail(request, pk):
    try:
        sacrament = Sacrament.objects.get(pk=pk)
    except Sacrament.DoesNotExist:
        return Response({'error': 'Sacrament record not found'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = SacramentSerializer(sacrament)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = SacramentSerializer(sacrament, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        sacrament.delete()
        return Response({'message': 'Sacrament record deleted'})

# Pledge Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def pledges(request):
    if request.method == 'GET':
        status_filter = request.GET.get('status', '')
        member_id = request.GET.get('member', '')
        
        pledges = Pledge.objects.all()
        
        if status_filter:
            pledges = pledges.filter(status=status_filter)
        if member_id:
            pledges = pledges.filter(member_id=member_id)
        
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def pledge_detail(request, pk):
    try:
        pledge = Pledge.objects.get(pk=pk)
    except Pledge.DoesNotExist:
        return Response({'error': 'Pledge not found'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PledgeSerializer(pledge)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = PledgeSerializer(pledge, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        pledge.delete()
        return Response({'message': 'Pledge deleted'})

# Payment Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def payments(request):
    if request.method == 'GET':
        pledge_id = request.GET.get('pledge', '')
        payments = Payment.objects.all()
        
        if pledge_id:
            payments = payments.filter(pledge_id=pledge_id)
        
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Dashboard Data
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    total_members = Member.objects.filter(is_active=True).count()
    
    # Sacrament counts
    baptism_count = Sacrament.objects.filter(sacrament_type='Baptism').count()
    confirmation_count = Sacrament.objects.filter(sacrament_type='Confirmation').count()
    marriage_count = Sacrament.objects.filter(sacrament_type='Marriage').count()
    
    # Pledge statistics
    total_pledges = Pledge.objects.aggregate(total=Sum('amount_promised'))['total'] or 0
    total_paid = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0
    outstanding_balance = total_pledges - total_paid
    
    unpaid_pledges = Pledge.objects.filter(status='Unpaid').count()
    partially_paid = Pledge.objects.filter(status='Partially Paid').count()
    fully_paid = Pledge.objects.filter(status='Fully Paid').count()
    
    # Recent activities
    recent_members = Member.objects.filter(is_active=True).order_by('-date_registered')[:5]
    recent_payments = Payment.objects.all().order_by('-payment_date')[:5]
    
    return Response({
        'total_members': total_members,
        'sacraments': {
            'baptism': baptism_count,
            'confirmation': confirmation_count,
            'marriage': marriage_count,
        },
        'pledges': {
            'total_pledged': total_pledges,
            'total_paid': total_paid,
            'outstanding': outstanding_balance,
            'unpaid': unpaid_pledges,
            'partially_paid': partially_paid,
            'fully_paid': fully_paid,
        },
        'recent_members': MemberSerializer(recent_members, many=True).data,
        'recent_payments': PaymentSerializer(recent_payments, many=True).data,
    })

# Reports
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reports(request):
    report_type = request.GET.get('type', '')
    
    if report_type == 'members':
        members = Member.objects.filter(is_active=True)
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)
    
    elif report_type == 'sacraments':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        sacraments = Sacrament.objects.all()
        if start_date:
            sacraments = sacraments.filter(date_received__gte=start_date)
        if end_date:
            sacraments = sacraments.filter(date_received__lte=end_date)
        
        serializer = SacramentSerializer(sacraments, many=True)
        return Response(serializer.data)
    
    elif report_type == 'pledges':
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)
    
    return Response({'error': 'Invalid report type'}, 
                   status=status.HTTP_400_BAD_REQUEST)