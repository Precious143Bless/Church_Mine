from django.contrib import admin
from .models import Member, Sacrament, Pledge, Payment

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'gender', 'civil_status', 'contact_number', 'date_registered']
    search_fields = ['first_name', 'last_name', 'email', 'contact_number']
    list_filter = ['gender', 'civil_status', 'is_active']

@admin.register(Sacrament)
class SacramentAdmin(admin.ModelAdmin):
    list_display = ['member', 'sacrament_type', 'date_received', 'officiating_priest']
    search_fields = ['member__first_name', 'member__last_name', 'certificate_number']
    list_filter = ['sacrament_type', 'date_received']

@admin.register(Pledge)
class PledgeAdmin(admin.ModelAdmin):
    list_display = ['member', 'pledge_description', 'amount_promised', 'status', 'due_date']
    search_fields = ['member__first_name', 'member__last_name', 'pledge_description']
    list_filter = ['status', 'due_date']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['pledge', 'amount', 'payment_date', 'payment_method', 'received_by']
    search_fields = ['pledge__member__first_name', 'pledge__member__last_name', 'receipt_number']
    list_filter = ['payment_method', 'payment_date']