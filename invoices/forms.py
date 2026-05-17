from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import (
    CompanyProfile,
    Customer,
    Product,
    Invoice
)


class CompanyProfileForm(forms.ModelForm):

    class Meta:
        model = CompanyProfile
        exclude = ['user']


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        exclude = ['user']


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ['user']


class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice

        fields = [
            'customer',
            'invoice_date',
            'due_date',
            'discount',
            'notes'
        ]

        widgets = {
            'invoice_date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'due_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }


# =========================
# USER SIGNUP FORM
# =========================

class SignUpForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:

        model = User

        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )