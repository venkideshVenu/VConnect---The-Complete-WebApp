from django import forms
from .models import Comment, PostReport, Post, UserReport

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write a comment...'}),
        }

class ReportPostForm(forms.ModelForm):
    class Meta:
        model = PostReport
        fields = ['reason']

class ReportUserForm(forms.ModelForm):
    class Meta:
        model = UserReport
        fields = ['reason']