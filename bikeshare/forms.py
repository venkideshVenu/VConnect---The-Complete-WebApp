from django import forms
from .models import Station, BikeShareProfile

class TopUpForm(forms.Form):
    money = forms.FloatField(label='Top Up Amount', max_value=100.0, min_value=5.0)

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