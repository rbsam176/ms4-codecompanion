from django.http import HttpResponse

from .models import Order, OrderLineItem
from services.models import Service

import json
import time

class StripeWH_Handler:
    """Handles Stripe web-hooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """Handles an unknown webhook event"""
        return HttpResponse(
            content=f'Unknown webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """Handles payment intent success from Stripe webhook """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        
        order_exists = False
        attempt = 1
        while attempt < 5:
            try:
                order = Order.objects.get(
                    email_address__iexact=intent.receipt_email,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order in database',
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    email_address=intent.receipt_email,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                for service_name, quantity in json.loads(bag).items():
                    service = Service.objects.get(pk=service_name)
                    order_line_item = OrderLineItem(
                        service=service,
                        quantity=quantity,
                        order=order,
                    )
                    order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(content=f'Webhook received: {event["type"]} | ERROR: {e}', status=500)

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """Handles payment intent failure from Stripe webhook """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)