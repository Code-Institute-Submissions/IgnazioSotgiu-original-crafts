from django.http import HttpResponse

# code taken from code institute lecture


class WebhookHandler():
    # handle webhood from stripe

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        # handle a webhook event

        return HttpResponse(
            content=f'Generic webhook received {event["type"]}',
            status=200,
        )

    def handle_payment_succeeded(self, event):
        # handle a webhook payment succeeded event

        return HttpResponse(
            content=f'Webhook received {event["type"]}',
            status=200,
        )

    def handle_payment_failed(self, event):
        # handle a webhook payment failed event

        return HttpResponse(
            content=f'Webhook received {event["type"]}',
            status=200,
        )
