from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db.models import Count, Sum, Q
import json
import os

def serve_index(request):
    """Serve the main index.html"""
    return render(request, 'index.html')

def serve_html(request, filename):
    """Serve HTML files from frontend folder"""
    try:
        return render(request, filename)
    except Exception as e:
        return HttpResponse(f"""
        <h1>Error Loading {filename}</h1>
        <p>Error: {str(e)}</p>
        <p>Template directories:</p>
        <ul>
            {''.join([f'<li>{d}</li>' for d in request.META.get('template_dirs', [])])}
        </ul>
        <a href="/">Go back</a>
        """, status=404)

def debug_files(request):
    """Debug endpoint to check file structure"""
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    
    frontend_path = os.path.join(base_dir, 'frontend')
    assets_path = os.path.join(frontend_path, 'assets')
    style_path = os.path.join(assets_path, 'style')
    scripts_path = os.path.join(assets_path, 'scripts')
    
    html_files = ['login.html', 'dashboard.html', 'members.html', 'member-detail.html', 
                  'member-form.html', 'sacraments.html', 'pledges.html', 'payments.html', 'reports.html']
    
    result = {
        'base_dir': base_dir,
        'frontend_exists': os.path.exists(frontend_path),
        'html_files': {},
        'assets': {
            'style.css_exists': os.path.exists(os.path.join(style_path, 'style.css')),
            'app.js_exists': os.path.exists(os.path.join(scripts_path, 'app.js')),
        }
    }
    
    for file in html_files:
        file_path = os.path.join(frontend_path, file)
        result['html_files'][file] = os.path.exists(file_path)
    
    return JsonResponse(result)

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
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        })
    else:
        return Response({'error': 'Invalid credentials'}, 
                       status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({'message': 'Logged out successfully'})

# Dashboard
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    from .models import Member, Sacrament, Pledge, Payment
    
    total_members = Member.objects.filter(is_active=True).count()
    baptism_count = Sacrament.objects.filter(sacrament_type='Baptism').count()
    confirmation_count = Sacrament.objects.filter(sacrament_type='Confirmation').count()
    marriage_count = Sacrament.objects.filter(sacrament_type='Marriage').count()
    
    total_pledged = Pledge.objects.aggregate(total=Sum('amount_promised'))['total'] or 0
    total_paid = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0
    
    return Response({
        'total_members': total_members,
        'sacraments': {
            'baptism': baptism_count,
            'confirmation': confirmation_count,
            'marriage': marriage_count,
        },
        'pledges': {
            'total_pledged': total_pledged,
            'total_paid': total_paid,
            'outstanding': total_pledged - total_paid,
        }
    })

# Member Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def members(request):
    from .models import Member
    from .serializers import MemberSerializer
    
    if request.method == 'GET':
        search = request.GET.get('search', '')
        members = Member.objects.filter(is_active=True)
        
        if search:
            members = members.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
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
    from .models import Member
    from .serializers import MemberSerializer
    
    try:
        member = Member.objects.get(pk=pk)
    except Member.DoesNotExist:
        return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
    
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