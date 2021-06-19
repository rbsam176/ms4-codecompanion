from django.http import HttpResponse

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
        print(intent)
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """Handles payment intent failure from Stripe webhook """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)