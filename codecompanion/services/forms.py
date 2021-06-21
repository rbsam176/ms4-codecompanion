from django import forms
from .models import Service, PriceType

class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        price_types = PriceType.objects.all()
        print(price_types)
        friendly_names = [(type.id, type.get_friendly_name()) for type in price_types]
        print(friendly_names)

        self.fields['price_type'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
