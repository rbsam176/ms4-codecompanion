from django import forms
from faq.models import FaqEntry

class AddUserFaq(forms.ModelForm):
    class Meta:
        model = FaqEntry
        fields = ('category', 'title', 'content',)
    
    def __init__(self, *args, **kwargs):
        """ Ensure fields are required """
        # SOURCE https://stackoverflow.com/a/53956528
        self._faq_question = kwargs.pop('faq_question', None)
        self._faq_category = kwargs.pop('faq_category', None)
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['required'] = True
        faq_question = self._faq_question
        faq_category = self._faq_category
        if faq_question and faq_category:
            self.initial['category'] = faq_category
            self.initial['title'] = faq_question
        self.fields['title'].widget.attrs['required'] = True
        self.fields['content'].widget.attrs['required'] = True