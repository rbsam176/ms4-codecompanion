from django.db import models

class FaqCategory(models.Model):
    category = models.CharField(max_length=254)

    def __str__(self):
        return self.category


class FaqEntry(models.Model):
    category = models.ForeignKey('FaqCategory', null=True, blank=False, on_delete=models.SET_NULL)
    title = models.CharField(max_length=254, null=True, blank=False)
    content = models.TextField(null=True, blank=False)
    clickCount = models.DecimalField(max_digits=10, decimal_places=0, null=False, default=0)
    
    def __str__(self):
        return self.title or ''
    
    def get_faq_category(self):
        return self.category

    def get_faq_content(self):
        return self.content