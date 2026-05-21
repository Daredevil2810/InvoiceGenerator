from django.urls import path

from . import views

urlpatterns = [

    path('', views.landing_page, name='landing_page'),

    path(
        'admin-dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'approve-user/<int:pk>/',
        views.approve_user,
        name='approve_user'
    ),

    path(
        'delete-user/<int:pk>/',
        views.delete_user,
        name='delete_user'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'demo-login/',
        views.demo_login,
        name='demo_login'
    ),

    path(
        'create-invoice/',
        views.create_invoice,
        name='create_invoice'
    ),

    path(
        'invoice/<int:pk>/',
        views.invoice_detail,
        name='invoice_detail'
    ),

    path(
        'customers/',
        views.customer_list,
        name='customer_list'
    ),

    path(
        'customer-invoices/<int:pk>/',
        views.customer_invoices,
        name='customer_invoices'
    ),

    path(
        'add-customer/',
        views.add_customer,
        name='add_customer'
    ),

    path(
        'edit-customer/<int:pk>/',
        views.edit_customer,
        name='edit_customer'
    ),

    path(
        'delete-customer/<int:pk>/',
        views.delete_customer,
        name='delete_customer'
    ),

    path(
        'products/',
        views.product_list,
        name='product_list'
    ),

    path(
        'add-product/',
        views.add_product,
        name='add_product'
    ),

    path(
        'edit-product/<int:pk>/',
        views.edit_product,
        name='edit_product'
    ),

    path(
        'delete-product/<int:pk>/',
        views.delete_product,
        name='delete_product'
    ),

    path(
        'company-profile/',
        views.company_profile,
        name='company_profile'
    ),

    path(
    'delete-invoice/<int:pk>/',
    views.delete_invoice,
    name='delete_invoice'
    ),

    path(
    'signup/',
    views.signup_view,
    name='signup'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
        'invoice/<int:pk>/cancel/',
        views.cancel_invoice,
        name='cancel_invoice'
    ),

]