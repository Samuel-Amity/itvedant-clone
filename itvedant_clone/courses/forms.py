from django import forms
from .models import Chapter

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['course', 'title', 'content', 'question', 'answer', 'hint']
