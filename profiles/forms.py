from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """ Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field """
        super().__init__(*args, **kwargs)
        placeholders = {
            'email_address': 'Email Address',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }

        self.fields['email_address'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False