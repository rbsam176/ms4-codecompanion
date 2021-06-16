from django.db import models

class PriceType(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

class Service(models.Model):
    """ A model to represent every service offered """
    icon = models.CharField(max_length=254)
    name = models.CharField(max_length=254, primary_key=True)
    endpoint = models.CharField(max_length=254, default='#')
    description = models.CharField(max_length=254)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    price_type = models.ForeignKey('PriceType', null=True, blank=True, on_delete=models.SET_NULL)
    bullet_point_1 = models.CharField(max_length=254, null=True, blank=True)
    bullet_point_2 = models.CharField(max_length=254, null=True, blank=True)
    bullet_point_3 = models.CharField(max_length=254, null=True, blank=True)
    bullet_point_4 = models.CharField(max_length=254, null=True, blank=True)

    def get_icon(self):
        return self.icon

    def __str__(self):
        return self.name

    def get_endpoint(self):
        return self.get_endpoint

    def get_description(self):
        return self.description

    def get_price(self):
        return self.price
    
    def get_price_type(self):
        return self.price_type
    
    def get_bullet_point_1(self):
        return self.bullet_point_1

    def get_bullet_point_2(self):
        return self.bullet_point_2
    
    def get_bullet_point_3(self):
        return self.bullet_point_3
    
    def get_bullet_point_4(self):
        return self.bullet_point_4