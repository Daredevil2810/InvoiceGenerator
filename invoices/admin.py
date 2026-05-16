from django.contrib import admin
from .models import UserProfile

from .models import (
    CompanyProfile,
    Customer,
    Product,
    Invoice,
    InvoiceItem
)


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):

    list_display = (
        'invoice_number',
        'customer',
        'invoice_date',
        'grand_total'
    )

    search_fields = (
        'invoice_number',
        'customer__customer_name'
    )

    list_filter = (
        'invoice_date',
    )

    inlines = [InvoiceItemInline]


admin.site.register(CompanyProfile)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(UserProfile)