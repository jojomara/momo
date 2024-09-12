from django.forms import ModelForm # type: ignore
from .models import *
from django import forms # type: ignore


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'

class AddStockForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, label="Quantity to Add")

    class Meta:
        model = Product
        fields = []  # Leave this empty as we are manually adding fields.



class ProcurementForm(forms.Form):
    produce_name = forms.CharField(max_length=100)
    produce_type = forms.CharField(max_length=50)
    date = forms.DateField()
    time = forms.TimeField()
    tonnage = forms.DecimalField(max_digits=10, decimal_places=2)
    cost = forms.DecimalField(max_digits=10, decimal_places=2)
    dealer_name = forms.CharField(max_length=100)
    branch_name = forms.CharField(max_length=100)
    contact = forms.CharField(max_length=15)

# forms.py (add this to the existing file)
class CreditSaleForm(forms.ModelForm):
    class Meta:
        model = CreditSale
        fields = '__all__'


# forms.py (update the ProcurementForm)
class ProcurementForm(forms.Form):
    PRODUCE_CHOICES = [
        ('beans', 'Beans'),
        ('maize', 'Maize'),
        ('soybeans', 'Soybeans'),
        # Add more produce options here
    ]
    produce_name = forms.ChoiceField(choices=PRODUCE_CHOICES)
    # Other fields remain the same



    

