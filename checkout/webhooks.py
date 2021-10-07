# code taken from stripe docs
import stripe
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import WebhookHandler

# code taken from code institute lecture


@require_POST
@csrf_exempt
def webhook_view(request):
    webhook_endpoint_secret = settings.WEBHOOK_ENDPOINT_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_endpoint_secret)

    except ValueError as e:
        # Invalid payload
        return HttpResponse(content=e, status=400)

    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(content=e, status=400)

    except Exception as e:
        # All other exceptions
        return HttpResponse(content=e, status=400)

    # connect to webhook handler

    handler = WebhookHandler(request)

    # connect methods to handle stripe webhook events

    event_connect = {
        'payment_intent.succeeded': handler.handle_payment_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_failed,
    }

    # event from stripe
    event_type = event['type']

    event_handler = event_connect.get(event_type, handler.handle_event)

    # call the method to handle the event

    response = event_handler(event)
    return response
