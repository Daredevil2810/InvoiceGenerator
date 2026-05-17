from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# =========================
# COMPANY PROFILE MODEL
# =========================

class CompanyProfile(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    
    company_name = models.CharField(max_length=255)

    address = models.TextField()

    gst_number = models.CharField(max_length=100)

    phone = models.CharField(max_length=20)

    email = models.EmailField(blank=True, null=True)

    website = models.CharField(max_length=255, blank=True, null=True)

    bank_name = models.CharField(max_length=255)

    account_number = models.CharField(max_length=100)

    ifsc_code = models.CharField(max_length=50)

    branch = models.CharField(max_length=255)

    upi_id = models.CharField(max_length=255, blank=True, null=True)

    terms_conditions = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.company_name


# =========================
# CUSTOMER MODEL
# =========================

class Customer(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    customer_name = models.CharField(max_length=255)

    company_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    address = models.TextField()

    state = models.CharField(max_length=100)

    city = models.CharField(max_length=100)

    pincode = models.CharField(max_length=20)

    gst_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name


# =========================
# PRODUCT MODEL
# =========================

class Product(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product_name = models.CharField(max_length=255)

    hsn_sac = models.CharField(max_length=100)

    gst_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name


# =========================
# INVOICE MODEL
# =========================

class Invoice(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    invoice_number = models.CharField(
        max_length=100,
        # unique=True
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    customer_name = models.CharField(
        max_length=255
    )

    customer_company = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    customer_address = models.TextField()

    customer_city = models.CharField(
        max_length=100
    )

    customer_state = models.CharField(
        max_length=100
    )

    customer_pincode = models.CharField(
        max_length=20
    )

    customer_gst = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    customer_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    customer_email = models.EmailField(
        blank=True,
        null=True
    )

    invoice_date = models.DateField()

    due_date = models.DateField(
        blank=True,
        null=True
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    cgst = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    sgst = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    igst = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    grand_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    PAYMENT_CHOICES = [

        ('Cash', 'Cash'),

        ('Bank Transfer', 'Bank Transfer'),

        ('UPI', 'UPI'),

        ('Online', 'Online'),

    ]

    payment_method = models.CharField(

        max_length=50,

        choices=PAYMENT_CHOICES,

        default='Cash'

    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number


# =========================
# INVOICE ITEM MODEL
# =========================

class InvoiceItem(models.Model):

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    description = models.CharField(max_length=255)

    hsn_sac = models.CharField(max_length=100)

    quantity = models.PositiveIntegerField()

    rate = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    gst_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    def save(self, *args, **kwargs):

        self.amount = Decimal(self.quantity) * Decimal(self.rate)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.invoice.invoice_number} - {self.description}'
    

# =========================
# USER PROFILE MODEL
# =========================

class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    is_demo_user = models.BooleanField(
        default=False
    )

    demo_created_at = models.DateTimeField(
        blank=True,
        null=True
    )

    is_approved = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.user.username


# =========================
# AUTO CREATE USER PROFILE
# =========================

@receiver(post_save, sender=User)
def create_user_profile(
    sender,
    instance,
    created,
    **kwargs
):

    if created:

        UserProfile.objects.create(
            user=instance
        )