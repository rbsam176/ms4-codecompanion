from django import forms
from .models import FaqEntry, FaqQuestion

class FaqForm(forms.ModelForm):
    class Meta:
        model = FaqEntry
        fields = ('category', 'title', 'content',)
    
    def __init__(self, *args, **kwargs):
        """ Ensure fields are required """
        # SOURCE https://stackoverflow.com/a/53956528
        self._header_id = kwargs.pop('header_id', None)
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['required'] = True
        header_id = self._header_id
        if header_id:
            self.initial['category'] = header_id
        self.fields['title'].widget.attrs['required'] = True
        self.fields['content'].widget.attrs['required'] = True


class NewFaq(forms.ModelForm):
    class Meta:
        model = FaqQuestion
        fields = ('category', 'question',)
    
    def __init__(self, *args, **kwargs):
        """ Ensure fields are required """
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['required'] = True
        self.fields['question'].widget.attrs['required'] = True