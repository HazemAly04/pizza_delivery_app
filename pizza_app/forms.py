from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm, ModelChoiceField
from django.db import transaction
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from datetime import datetime


class UserSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        error_messages = {
            'username': {
                'unique': "A user with that email already exists.",
            }
        }

    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'johndoe@example.com'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = False
        user.email = self.cleaned_data['username']
        user.save()
        return user
    
    def clean(self):
        data = self.cleaned_data
        email = data['username']
        if email:
            try:
                validate_email(email)
            except ValidationError:
                self.add_error('username', 'This is not a valid email')
            else:
                try:
                    user = User.objects.get(email=email)           # had to move this chunk here as getting username outside the if caused erros
                    #user = User.objects.filter(email=email).first()
                    if user.is_superuser:
                        self.add_error('username', 'A user with that email already exists.') # its a superuser but can't say that in the error message
                except ObjectDoesNotExist:
                    pass
        return data


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'johndoe@example.com'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })


class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = '__all__'

        widgets = {
            'pepperoni': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'chicken': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ham': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pineapple': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'peppers': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'mushrooms': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'onions': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'olives': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'size': forms.Select(attrs={'class': 'form-select'}),
            'crust': forms.Select(attrs={'class': 'form-select'}),
            'sauce': forms.Select(attrs={'class': 'form-select'}),
            'cheese': forms.Select(attrs={'class': 'form-select'}),
        }


def capitalize_each_word(value):
    return value.title()

def format_eircode(value):
    value = value.upper().replace(" ", "")
    return value[:3] + " " + value[3:]

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'county': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'County'}),
            'eircode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Eircode'}),
            'card': forms.NumberInput(attrs={'class': 'form-control no-spinners', 'placeholder': 'Card Number'}),
            'name_on_card': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name on Card'}),
            'cvv': forms.NumberInput(attrs={'class': 'form-control no-spinners', 'placeholder': 'CVV'}),
            'expiry': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'}),
        }

    def clean(self):
        data = self.cleaned_data
        name = data['name']
        street = data['street']
        city = data['city']
        county = data['county']
        eircode = data['eircode']
        name_on_card = data['name_on_card']
        card = data['card']
        cvv = data['cvv']
        expiry = data['expiry']

        data['name'] = capitalize_each_word(name)
        data['street'] = capitalize_each_word(street)
        data['city'] = capitalize_each_word(city)
        data['county'] = capitalize_each_word(county)
        data['name_on_card'] = capitalize_each_word(name_on_card)


        if len(eircode) != 7:
            self.add_error('eircode', 'This is not a valid eircode (it must be 7 characters long)')
        if len(str(card)) != 16:
            self.add_error('card', 'This is not a valid card number (it must be 16 characters long)')
        if len(str(cvv)) != 3:
            self.add_error('cvv', 'This is not a valid CVV (it must be 3 characters long)')
        if len(expiry) != 5:
            self.add_error('expiry', 'This is not a valid expiry date (it must be in the format MM/YY)')
        else: 
            month, year = expiry.split('/')
            if not month.isdigit() or not year.isdigit():
                self.add_error('expiry', 'This is not a valid expiry date (it contains non-numeric characters)')
            else:
                month, year = int(month), int(year) + 2000

                if month < 1 or month > 12:
                    # raise forms.ValidationError("This is not a valid expiry date")
                    self.add_error('expiry', 'This card has already expired')
                if year < datetime.now().year or (year == datetime.now().year and month < datetime.now().month):
                    # raise forms.ValidationError('This is not a valid expiry date')
                    self.add_error('expiry', 'This card has already expired')

        return data

