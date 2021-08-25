from django import forms
from .models import UserProfile, CompanionProfile
from django.contrib.auth.models import User
import datetime
import pytz

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)
    
    def __init__(self, *args, **kwargs):
        """ Add asterisk to email field label and make it required """
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['required'] = True
            self.fields[field].label = f'{self.fields[field].label} *'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CompanionProfile
        exclude = ['user']
    

    def __init__(self, *args, **kwargs):
        """ Sets custom labels/placeholders """
        super().__init__(*args, **kwargs)
        # BIO
        self.fields['bio'].label = "Your bio"
        self.fields['bio'].widget.attrs['placeholder'] = "Write a little about yourself and your professional experience so students can determine if you would be the best fit for them."
        
        # AVAILABILTY & SERVICES CUSTOM LABELS
        for field in self.fields:
            if '_available' in field:
                self.fields[field].label = field.replace('_available', '').replace('_', ' ').capitalize()


class CompanionCheck(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        """ Sets custom label and applies class to checkbox """
        super().__init__(*args, **kwargs)
        self.fields['is_companion'].label = "I'd like to become a companion"
        self.fields['is_companion'].widget.attrs['class'] = "convert-toggle"

    # def __init__(self, *args, **kwargs):
    #     """ Add placeholders and classes, remove auto-generated
    #     labels and set autofocus on first field """
        # super().__init__(*args, **kwargs)
        # print(self)
        # self.fields['is_companion'].label = "Companion?"
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
            # self.fields[field].widget.attrs['class'] = 'stripe-style-input'
        #         self.fields[field].label = False
        # self.fields['is_companion'].label = "Companion?"