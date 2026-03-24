from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Member(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    CIVIL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Widowed', 'Widowed'),
        ('Divorced', 'Divorced'),
    ]
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=20, blank=True)
    
    # Basic Details
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    civil_status = models.CharField(max_length=20, choices=CIVIL_STATUS_CHOICES)
    
    # Contact Information
    address = models.TextField()
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    
    # Additional Info
    occupation = models.CharField(max_length=100, blank=True)
    spouse_name = models.CharField(max_length=200, blank=True)
    date_registered = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name} {self.suffix}".strip()
    
    class Meta:
        ordering = ['last_name', 'first_name']

class Sacrament(models.Model):
    SACRAMENT_TYPES = [
        ('Baptism', 'Baptism'),
        ('Confirmation', 'Confirmation'),
        ('First Holy Communion', 'First Holy Communion'),
        ('Marriage', 'Marriage'),
        ('Last Rites', 'Last Rites'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='sacraments')
    sacrament_type = models.CharField(max_length=50, choices=SACRAMENT_TYPES)
    date_received = models.DateField()
    officiating_priest = models.CharField(max_length=200)
    church_location = models.CharField(max_length=200, blank=True)
    
    # Baptism specific
    godfather = models.CharField(max_length=200, blank=True)
    godmother = models.CharField(max_length=200, blank=True)
    
    # Confirmation specific
    confirmation_name = models.CharField(max_length=100, blank=True)
    sponsor = models.CharField(max_length=200, blank=True)
    
    # Marriage specific
    spouse = models.CharField(max_length=200, blank=True)
    witnesses = models.TextField(blank=True, help_text="Names of witnesses, one per line")
    
    # Common fields
    remarks = models.TextField(blank=True)
    certificate_number = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sacrament_type} - {self.member.full_name}"
    
    class Meta:
        ordering = ['-date_received']

class Pledge(models.Model):
    STATUS_CHOICES = [
        ('Unpaid', 'Unpaid'),
        ('Partially Paid', 'Partially Paid'),
        ('Fully Paid', 'Fully Paid'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='pledges')
    pledge_description = models.CharField(max_length=200)
    amount_promised = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    pledge_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Unpaid')
    notes = models.TextField(blank=True)
    
    @property
    def total_paid(self):
        return self.payments.aggregate(total=models.Sum('amount'))['total'] or 0
    
    @property
    def balance(self):
        return self.amount_promised - self.total_paid
    
    def update_status(self):
        if self.balance <= 0:
            self.status = 'Fully Paid'
        elif self.total_paid > 0:
            self.status = 'Partially Paid'
        else:
            self.status = 'Unpaid'
        self.save(update_fields=['status'])
    
    def __str__(self):
        return f"{self.member.full_name} - {self.pledge_description}"
    
    class Meta:
        ordering = ['-pledge_date']

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('Check', 'Check'),
        ('Online Transfer', 'Online Transfer'),
        ('GCash', 'GCash'),
    ]
    
    pledge = models.ForeignKey(Pledge, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    reference_number = models.CharField(max_length=100, blank=True)
    received_by = models.CharField(max_length=100)
    receipt_number = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.pledge.update_status()
    
    def __str__(self):
        return f"Payment for {self.pledge.member.full_name} - {self.amount}"
    
    class Meta:
        ordering = ['-payment_date']