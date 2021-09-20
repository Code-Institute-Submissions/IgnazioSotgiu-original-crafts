from django.http import HttpResponse

# code taken from code institute lecture


class WebhookHandler():
    # handle webhood from stripe

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        # handle a webhook event

        return HttpResponse(
            content=f'Webhook received {event["type"]}',
            status=200,
        )
