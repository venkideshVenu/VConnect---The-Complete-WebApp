from django import forms
from .models import Profile, Skill

from django import forms
from jobprofile.models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'is_employer', 'gender', 'education', 'short_intro', 'bio', 
            'location', 'social_github', 'social_linkedin', 'social_twitter', 
            'social_website', 'social_youtube'
        ]
        widgets = {
            'is_employer': forms.Select(choices=[
                (None, "Select Role"),
                (True, "Employer"),
                (False, "Job Seeker")
            ])
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input'

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input'