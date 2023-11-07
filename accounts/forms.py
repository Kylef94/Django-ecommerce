from django.forms import ModelForm


from .models import *

class CustomerCreationForm(ModelForm):
    
    class Meta:
        model = Customer
        fields = ['email', 'password', 'first_name', 'last_name']

class CustomerChangeForm(ModelForm):
    
    class Meta:
        model = Customer
        fields = ['email', 'first_name', 'last_name']
        
class AddressForm(ModelForm):
    
    class Meta:
        model = Address
        fields = ['line_1', 'line_2', 'city', 'region', 'country', 'postcode']