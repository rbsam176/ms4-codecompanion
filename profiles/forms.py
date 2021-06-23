from django import forms
from .models import UserProfile
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)
    
    def __init__(self, *args, **kwargs):
        """ Add asterisk to email field label and make it required """
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['required'] = True
        self.fields['email'].label = "Email Address*"

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']

class CompanionCheck(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['is_companion']

    # def __init__(self, *args, **kwargs):
    #     """ Add placeholders and classes, remove auto-generated
    #     labels and set autofocus on first field """
        # super().__init__(*args, **kwargs)
        # placeholders = {
        #     'email_address': 'Email Address',
        #     'first_name': 'First Name',
        #     'last_name': 'Last Name',
        # }

        # self.fields['email_address'].widget.attrs['autofocus'] = True
        # for field in self.fields:
        #     if field in placeholders:
        #         if self.fields[field].required:
        #             placeholder = f'{placeholders[field]} *'
        #         else:
        #             placeholder = placeholders[field]
        #         self.fields[field].widget.attrs['placeholder'] = placeholder
        #         # self.fields[field].widget.attrs['class'] = 'stripe-style-input'
        #         self.fields[field].label = False
        # self.fields['is_companion'].label = "Companion?"