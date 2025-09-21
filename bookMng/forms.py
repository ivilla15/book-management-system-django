from django import forms
from django.forms import ModelForm
from .models import Book
from django import forms
from .models import Comment

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'web',
            'price',
            'picture',
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    content = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Write a comment...', 'rows': 4, 'cols': 50}),
        label=''
    )
