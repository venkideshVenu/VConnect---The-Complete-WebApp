from django import forms
from .models import Station, BikeShareProfile

from django import forms

# forms.py
class TopUpForm(forms.Form):
    amount = forms.DecimalField(
        min_value=0.01,
        max_value=1000.00,  # Optional: set maximum top-up amount
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter amount to top up',
            'min': '0.01',
            'step': '0.01'
        })
    )

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than 0")
        return amount

class PayBalanceForm(forms.Form):
    money = forms.FloatField(label='Payment Amount')

class LocationForm(forms.ModelForm):
    locations = forms.ModelChoiceField(queryset=Station.objects.all(), label='Station Location')

    class Meta:
        model = Station
        fields = ['locations']


class RoleSelectionForm(forms.Form):
    ROLE_CHOICES = [
        ('Customer', 'Customer'),
        ('Operator', 'Operator'),
        ('Manager', 'Manager'),
    ]
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        label="Select your role"
    )