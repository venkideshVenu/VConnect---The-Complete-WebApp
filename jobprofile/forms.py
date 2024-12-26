from django import forms
from .models import Profile, Skill

from django import forms
from jobprofile.models import Profile, Message
from django.forms import ModelForm

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'gender', 'education', 'short_intro', 'bio', 
            'location', 'social_github', 'social_linkedin', 'social_twitter', 
            'social_website', 'social_youtube'
        ]

    def __init__(self, *args, **kwargs):
        is_employer = kwargs.pop('is_employer', None)
        super().__init__(*args, **kwargs)
        if is_employer:
            self.fields['company_name'] = forms.CharField(
                max_length=200,
                required=True,
                widget=forms.TextInput(attrs={'class': 'profile-input'}),
            )
        for field in self.fields.values():
            field.widget.attrs['class'] = 'profile-input'


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input'



class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
