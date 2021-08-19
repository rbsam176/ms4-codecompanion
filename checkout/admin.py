from django.contrib import admin
from .models import Order, OrderLineItem

class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total', 'start_datetime', 'end_datetime')

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = ('order_number', 'date', 
                       'order_total', 'original_bag', 'stripe_pid')

    fields = ('order_number', 'user_profile', 'date', 'notes',
              'order_total', 'original_bag', 'stripe_pid')

    list_display = ('order_number', 'date', 'notes',
              'order_total' )

    ordering = ('-date', )

admin.site.register(Order, OrderAdmin)