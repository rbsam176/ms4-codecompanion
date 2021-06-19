from django.http import HttpResponse

class StripeWH_Handerl:
    """Handles Stripe web-hooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """Handles an unknown webhook event"""
        return HttpResponse(
            context=f'Webhook received: {event["type"]}',
            status=200)