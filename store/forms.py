from django import forms
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Customer, Payment, Product, Review, Shippingaddress


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter username...'}),
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter password...'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Confirm password...'})

class ShippingForm(forms.ModelForm):
    class Meta:
        model = Shippingaddress
        fields = ['name', 'address', 'email', 'phone', 'city', 'pincode', 'state']
        field_args = {
            "name" : {
                "error_messages" : {
                    "required" : "Please let us know what to call you!"
                }
            }
        }
    def __init__(self, *args, **kwargs):
        super(ShippingForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'name'}),
        self.fields['address'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'address','rows': 1})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'email'})
        self.fields['phone'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'phone'}),
        self.fields['city'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'city'})
        self.fields['pincode'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'pincode'})
        self.fields['state'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'state' })


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        exclude = ['order']     
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'name', 'id':'name', 'type':'text'})
        self.fields['cardnumber'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': '0000 0000 0000 0000', 'id':'card', 'type':'text'}),
        self.fields['month'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'month', 'id':'month', 'type':'text'}),
        self.fields['year'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'year', 'id':'year', 'type':'text'}),
        self.fields['cvv'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'cvv', 'id':'cvv', 'type':'text'}),        

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['subject', 'content']
    
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        self.fields['subject'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'subject', 'id':'subject', 'type':'text'})

        self.fields['content'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'write your review', 'id':'review', 'rows': 4, })    

class CustomerForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Name', 'id':'subject', 'type':'text'})

        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'email', 'id':'subject', 'type':'text'})
