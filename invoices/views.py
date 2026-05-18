from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from num2words import num2words
from decimal import Decimal
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.functions import ExtractMonth, ExtractYear

from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .models import UserProfile

from .forms import SignUpForm

from .models import (
    CompanyProfile,
    Customer,
    Product,
    Invoice,
    InvoiceItem
)

from .forms import (
    CompanyProfileForm,
    CustomerForm,
    ProductForm,
    InvoiceForm
)

def check_demo_expiry(request):

    if request.user.is_authenticated:

        try:

            profile = UserProfile.objects.get(
                user=request.user
            )

            if profile.is_demo_user:

                now = timezone.now()

                diff = now - profile.demo_created_at

                if diff.total_seconds() > 600:

                    logout(request)

                    request.user.delete()

                    messages.error(
                        request,
                        'Demo expired after 10 minutes.'
                    )

                    return True

        except:
            pass

    return False

# =========================
# DASHBOARD
# =========================

@login_required
def dashboard(request):

    if check_demo_expiry(request):
        return redirect('landing_page')

    query = request.GET.get('q')

    month_filter = request.GET.get('month')
    year_filter = request.GET.get('year')

    invoices = Invoice.objects.filter(
        user=request.user
    ).order_by('-id')

    # SEARCH FILTER
    if query:

        invoices = invoices.filter(
            invoice_number__icontains=query
        )

    # MONTH FILTER
    if month_filter:

        year, month = month_filter.split('-')

        invoices = invoices.filter(
            invoice_date__year=year,
            invoice_date__month=month
        )

    # YEAR FILTER
    if year_filter:

        invoices = invoices.filter(
            invoice_date__year=year_filter
        )

    # TOTAL REVENUE
    total_revenue = sum(
        invoice.grand_total
        for invoice in invoices
    )

    context = {

        'invoices': invoices,

        'total_revenue': total_revenue

    }

    return render(
        request,
        'invoices/dashboard.html',
        context
    )

# =========================
# CUSTOMER
# =========================

@login_required
def customer_list(request):

    if check_demo_expiry(request):
        return redirect('landing_page')

    query = request.GET.get('q')

    customers = Customer.objects.filter(
                    user=request.user
                )

    if query:

        customers = customers.filter(
            company_name__icontains=query
        )

    return render(
        request,
        'invoices/customer_list.html',
        {
            'customers': customers,
            'query': query
        }
    )

def customer_invoices(request, pk):

    customer = get_object_or_404(
        Customer,
        pk=pk,
        user=request.user
    )

    query = request.GET.get('q')

    month_filter = request.GET.get('month')
    year_filter = request.GET.get('year')

    invoices = Invoice.objects.filter(
        customer=customer
    ).order_by('-id')

    # SEARCH
    if query:

        invoices = invoices.filter(
            invoice_number__icontains=query
        )

    # MONTH FILTER
    if month_filter:

        year, month = month_filter.split('-')

        invoices = invoices.filter(
            invoice_date__year=year,
            invoice_date__month=month
        )

    # YEAR FILTER
    if year_filter:

        invoices = invoices.filter(
            invoice_date__year=year_filter
        )

    total_revenue = sum(
        invoice.grand_total
        for invoice in invoices
    )

    context = {

        'customer': customer,

        'invoices': invoices,

        'total_revenue': total_revenue

    }

    return render(
        request,
        'invoices/customer_invoices.html',
        context
    )

@login_required
def add_customer(request):

    if check_demo_expiry(request):
        return redirect('landing_page')

    profile = UserProfile.objects.get(
        user=request.user
    )

    if profile.is_demo_user:

        if Customer.objects.filter(
            user=request.user
        ).count() >= 5:

            messages.error(
                request,
                'Demo limit reached. Max 5 customers allowed.'
            )

            return redirect('customer_list')

    form = CustomerForm(request.POST or None)

    if form.is_valid():
        customer = form.save(
            commit=False
        )

        customer.user = request.user

        customer.save()
        return redirect('customer_list')

    return render(
        request,
        'invoices/add_customer.html',
        {'form': form}
    )

def edit_customer(request, pk):

    customer = get_object_or_404(
        Customer,
        pk=pk,
        user=request.user
    )

    form = CustomerForm(
        request.POST or None,
        instance=customer
    )

    if form.is_valid():

        form.save()

        return redirect('customer_list')

    return render(
        request,
        'invoices/add_customer.html',
        {'form': form}
    )


def delete_customer(request, pk):

    customer = get_object_or_404(
        Customer,
        pk=pk,
        user=request.user
    )

    customer.delete()

    return redirect('customer_list')


# =========================
# PRODUCT
# =========================

@login_required
def product_list(request):

    if check_demo_expiry(request):
        return redirect('landing_page')

    query = request.GET.get('q')

    products = Product.objects.filter(
                    user=request.user
                )

    if query:

        products = products.filter(
            product_name__icontains=query
        )

    return render(
        request,
        'invoices/product_list.html',
        {
            'products': products,
            'query': query
        }
    )

@login_required
def add_product(request):

    if check_demo_expiry(request):
        return redirect('landing_page')

    profile = UserProfile.objects.get(
        user=request.user
    )

    if profile.is_demo_user:

        if Product.objects.filter(
            user=request.user
        ).count() >= 5:

            messages.error(
                request,
                'Demo limit reached. Max 5 products allowed.'
            )

            return redirect('product_list')

    form = ProductForm(request.POST or None)

    if form.is_valid():
        product = form.save(
            commit=False
        )

        product.user = request.user

        product.save()
        return redirect('product_list')

    return render(
        request,
        'invoices/add_product.html',
        {'form': form}
    )

def edit_product(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk,
        user=request.user
    )

    form = ProductForm(
        request.POST or None,
        instance=product
    )

    if form.is_valid():

        form.save()

        return redirect('product_list')

    return render(
        request,
        'invoices/add_product.html',
        {'form': form}
    )


def delete_product(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk,
        user=request.user
    )

    product.delete()

    return redirect('product_list')


# =========================
# COMPANY PROFILE
# =========================

@login_required
def company_profile(request):

    if check_demo_expiry(request):
        return redirect('landing_page')

    profile = CompanyProfile.objects.filter(
        user=request.user
    ).first()

    if profile:
        form = CompanyProfileForm(
            request.POST or None,
            request.FILES or None,
            instance=profile
        )
    else:
        form = CompanyProfileForm(
            request.POST or None,
            request.FILES or None
        )

    if form.is_valid():
        company = form.save(
            commit=False
        )

        company.user = request.user

        company.save()
        return redirect('company_profile')

    return render(
        request,
        'invoices/company_profile.html',
        {'form': form}
    )


# =========================
# CREATE INVOICE
# =========================

@login_required
def create_invoice(request):

    if check_demo_expiry(request):
        return redirect('landing_page')

    profile = UserProfile.objects.get(
        user=request.user
    )

    if profile.is_demo_user:

        if Invoice.objects.filter(
            user=request.user
        ).count() >= 5:

            messages.error(
                request,
                'Demo limit reached. Max 5 invoices allowed.'
            )

            return redirect('dashboard')

    customers = Customer.objects.filter(
                    user=request.user
                )
    products = Product.objects.filter(
                    user=request.user
                )

    if request.method == 'POST':

        customer_id = request.POST.get('customer')

        customer = Customer.objects.get(
            id=customer_id
        )

        invoice_count = Invoice.objects.filter(
                            user=request.user
                        ).count() + 1

        from datetime import datetime

        year = datetime.now().year

        invoice_number = (
        f'INV-{year}-{invoice_count:04d}'
        )

        invoice = Invoice.objects.create(
            user=request.user,
            customer_name=customer.customer_name,
            customer_company=customer.company_name,
            customer_address=customer.address,
            customer_city=customer.city,
            customer_state=customer.state,
            customer_pincode=customer.pincode,
            customer_gst=customer.gst_number,
            customer_phone=customer.phone,
            customer_email=customer.email,
            invoice_number=invoice_number,
            customer=customer,
            invoice_date=request.POST.get(
                'invoice_date'
            ),
            due_date=request.POST.get(
                'due_date'
            ),
            notes=request.POST.get('notes'),
            discount=Decimal(
                request.POST.get(
                    'discount',
                    0
                )
            ),
            payment_method = request.POST.get(
                'payment_method'
            )
        )

        product_ids = request.POST.getlist(
            'product[]'
        )

        hsn_codes = request.POST.getlist(
            'hsn[]'
        )

        quantities = request.POST.getlist(
            'quantity[]'
        )

        rates = request.POST.getlist(
            'rate[]'
        )

        gst_percents = request.POST.getlist(
            'gst[]'
        )

        subtotal = Decimal('0.00')

        total_gst = Decimal('0.00')

        for i in range(len(product_ids)):

            qty = int(quantities[i])

            rate = Decimal(rates[i])

            gst_percent = Decimal(
                gst_percents[i]
            )

            amount = qty * rate

            gst_amount = (
                amount * gst_percent
            ) / 100

            subtotal += amount

            total_gst += gst_amount

            # GET PRODUCT
            product = Product.objects.get(
                id=product_ids[i]
            )

            InvoiceItem.objects.create(

                invoice=invoice,

                product=product,

                description=product.product_name,

                hsn_sac=hsn_codes[i],

                quantity=qty,

                rate=rate,

                gst_percent=gst_percent,

                amount=amount
            )

        invoice.subtotal = subtotal

        # GET COMPANY PROFILE
        company_profile = CompanyProfile.objects.filter(
            user=request.user
        ).first()

        # GST LOGIC
        if company_profile and (
            company_profile.state_code == customer.state_code
        ):

            # SAME STATE → CGST + SGST
            invoice.cgst = total_gst / 2
            invoice.sgst = total_gst / 2
            invoice.igst = Decimal('0.00')

        else:

            # DIFFERENT STATE → IGST
            invoice.cgst = Decimal('0.00')
            invoice.sgst = Decimal('0.00')
            invoice.igst = total_gst

        # GRAND TOTAL
        invoice.grand_total = (
            subtotal
            + total_gst
            - invoice.discount
        )

        invoice.save()

        return redirect(
            'invoice_detail',
            pk=invoice.id
        )

    return render(
        request,
        'invoices/create_invoice.html',
        {
            'customers': customers,
            'products': products
        }
    )


# =========================
# INVOICE DETAIL
# =========================

@login_required
def invoice_detail(request, pk):

    if check_demo_expiry(request):
        return redirect('landing_page')

    invoice = get_object_or_404(

        Invoice,

        pk=pk,

        user=request.user
    )

    profile = CompanyProfile.objects.filter(
        user=request.user
    ).first()

    amount_in_words = num2words(
        invoice.grand_total,
        lang='en_IN'
    ).title() + ' Rupees Only'


    return render(
        request,
        'invoices/invoice_detail.html',
        {
            'invoice': invoice,
            'profile': profile,
            'amount_in_words': amount_in_words
        }
    )


@login_required
def delete_invoice(request, pk):

    invoice = get_object_or_404(
        Invoice,
        pk=pk
    )

    invoice.delete()

    return redirect('dashboard')


# =========================
# SIGNUP
# =========================

def signup_view(request):

    form = SignUpForm(
        request.POST or None
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Account created successfully. Wait for admin approval.'
        )

        return redirect('login')

    return render(
        request,
        'invoices/signup.html',
        {'form': form}
    )


# =========================
# LOGIN
# =========================

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            profile = UserProfile.objects.get(
                user=user
            )

            if profile.is_approved:

                login(request, user)

                return redirect(
                    'dashboard'
                )

            else:

                messages.error(
                    request,
                    'Your account is waiting for admin approval.'
                )

                return redirect('login')

        else:

            messages.error(
                request,
                'Invalid username or password'
            )

    return render(
        request,
        'invoices/login.html'
    )


# =========================
# LOGOUT
# =========================

def logout_view(request):

    logout(request)

    return redirect('login')

def landing_page(request):

    if request.user.is_authenticated:

        return redirect('dashboard')

    return render(
        request,
        'invoices/landing_page.html'
    )

def demo_login(request):

    unique_id = str(uuid.uuid4())[:8]

    username = f'demo_{unique_id}'

    password = 'demopassword123'

    user = User.objects.create_user(
        username=username,
        password=password
    )

    profile = UserProfile.objects.get(
        user=user
    )

    profile.is_approved = True
    profile.is_demo_user = True
    profile.demo_created_at = timezone.now()

    profile.save()

    login(request, user)

    return redirect('dashboard')

# =========================
# ADMIN DASHBOARD
# =========================

@staff_member_required
def admin_dashboard(request):

    pending_users = UserProfile.objects.filter(
        is_approved=False,
        is_demo_user=False
    )

    approved_users = UserProfile.objects.filter(
        is_approved=True,
        is_demo_user=False
    )

    demo_users = UserProfile.objects.filter(
        is_demo_user=True
    )

    total_invoices = Invoice.objects.count()

    total_customers = Customer.objects.count()

    total_products = Product.objects.count()

    context = {

        'pending_users': pending_users,

        'approved_users': approved_users,

        'demo_users': demo_users,

        'total_invoices': total_invoices,

        'total_customers': total_customers,

        'total_products': total_products
    }

    return render(
        request,
        'invoices/admin_dashboard.html',
        context
    )

# =========================
# APPROVE USER
# =========================

@staff_member_required
def approve_user(request, pk):

    profile = get_object_or_404(
        UserProfile,
        pk=pk
    )

    profile.is_approved = True

    profile.save()

    messages.success(
        request,
        f'{profile.user.username} approved successfully.'
    )

    return redirect('admin_dashboard')


# =========================
# DELETE USER
# =========================

@staff_member_required
def delete_user(request, pk):

    profile = get_object_or_404(
        UserProfile,
        pk=pk
    )

    username = profile.user.username

    profile.user.delete()

    messages.success(
        request,
        f'{username} deleted successfully.'
    )

    return redirect('admin_dashboard')