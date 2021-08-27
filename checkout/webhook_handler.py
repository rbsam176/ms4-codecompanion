from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

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


    def _send_confirmation_email(self, order):
        """ Send the user a confirmation email """
        cust_email = order.user_profile.user.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )


    def handle_payment_intent_succeeded(self, event):
        """Handles payment intent success from Stripe webhook """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag

        print('handle payment intent succeeded')
        
        order_exists = False
        attempt = 1
        while attempt < 5:
            try:
                order = Order.objects.get(
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            print("order exists")
            print(order)
            print('sending email')
            self._send_confirmation_email(order)
            print('sent')
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order in database',
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    original_bag=bag,
                    stripe_pid=pid,
                )
                for service_name in json.loads(bag).items():
                    service = Service.objects.get(pk=service_name)
                    order_line_item = OrderLineItem(
                        service=service,
                        order=order,
                    )
                    order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(content=f'Webhook received: {event["type"]} | ERROR: {e}', status=500)

        print('sending email below if')
        self._send_confirmation_email(order)
        print('sent')
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)


    def handle_payment_intent_payment_failed(self, event):
        """Handles payment intent failure from Stripe webhook """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)