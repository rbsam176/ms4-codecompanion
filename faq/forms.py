from django import forms
from .models import FaqEntry

class FaqForm(forms.ModelForm):
    class Meta:
        model = FaqEntry
        fields = ('category', 'title', 'content',)
    
    def __init__(self, *args, **kwargs):
        """ Ensure fields are required """
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['required'] = True
        self.fields['title'].widget.attrs['required'] = True
        self.fields['content'].widget.attrs['required'] = True