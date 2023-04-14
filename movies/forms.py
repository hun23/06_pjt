from django import forms
from .models import Movie, Comment

# 1) Moive
class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('title', 'description', )

# 2) Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('movie', 'user',)