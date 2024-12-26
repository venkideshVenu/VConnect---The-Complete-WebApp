from django import forms
from .models import JobModel, ApplicantModel

class JobForm(forms.ModelForm):
    class Meta:
        model = JobModel
        fields = [
            'title', 'description', 'requirements', 'responsibilities', 
            'qualifications', 'featured_image', 'company_logo',
            'company_name', 'company_description', 'company_website',
            'company_email', 'type', 'salary_range', 'location', 'deadline',
            'tags'
        ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 6}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
            'responsibilities': forms.Textarea(attrs={'rows': 4}),
            'qualifications': forms.Textarea(attrs={'rows': 4}),
        }

class ApplyJobForm(forms.ModelForm):
    class Meta:
        model = ApplicantModel
        fields = [] # No fields needed for this form