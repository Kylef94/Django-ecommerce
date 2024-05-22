from django import forms
from .models import Address
from django_countries.fields import CountryField

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["address_1", "address_2", "city", "postcode", "country", "address_type", "default"]
        
class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    house_number = forms.CharField(max_length=30)
    street_address = forms.CharField(max_length=30)
    city = forms.CharField(max_length=15)
    postcode = forms.CharField(max_length=10)
    country = CountryField(blank_label="Select Country").formfield()
    same_billing = forms.BooleanField(widget=forms.CheckboxInput())
    #save_info = forms.BooleanField(widget=forms.CheckboxInput())
    #payment = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
    