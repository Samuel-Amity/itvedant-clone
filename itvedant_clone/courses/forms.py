from django import forms
from .models import Chapter

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['course', 'title', 'content', 'question', 'answer', 'hint']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap class to form fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'    
