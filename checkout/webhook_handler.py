from django.http import HttpResponse
from .models import CheckoutOrder, OrderLineItem
from store.models import Product
import json
import time

# code structure taken from code institute lecture


class WebhookHandler():
    # handle webhood from stripe

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        # handle generic  webhook event

        return HttpResponse(
            content=f'Generic webhook received {event["type"]}',
            status=200,
        )

    def handle_payment_succeeded(self, event):
        # handle a webhook payment succeeded event

        # create the variables
        intent = event.data.object
        trolley = intent.metadata.trolley
        pid = intent.id
        save_address_details = intent.metadata.save_address_details
        billing_details = intent.charges.data[0].billing_details
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        checkout_order_exists = False
        checkout_order = None
        attempt = 1
        # check if order exists in database
        while attempt <= 5:
            try:
                checkout_order = CheckoutOrder.objects.get(
                    full_name__iexact=billing_details.name,
                    email_address__iexact=billing_details.email,
                    street_address__iexact=billing_details.address.line1,
                    town_or_city__iexact=billing_details.address.city,
                    county__iexact=billing_details.address.state,
                    zip_postcode__iexact=billing_details.address.postal_code,
                    country__iexact=billing_details.address.country,
                    order_trolley=trolley,
                    order_pid=pid,
                )

                checkout_order_exists = True
                break

            except CheckoutOrder.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if checkout_order_exists:
            return HttpResponse(
                content=f'Webhook received {event["type"]}.\
                    Found order in the database',
                status=200,
            )
        else:
            checkout_order = None
            # retrieve data order from webhook and save it
            try:
                checkout_order = CheckoutOrder.objects.create(
                    full_name=billing_details.name,
                    email_address=billing_details.email,
                    street_address=billing_details.address.line1,
                    town_or_city=billing_details.address.city,
                    county=billing_details.address.state,
                    zip_postcode=billing_details.address.postal_code,
                    country=billing_details.address.country,
                    order_trolley=trolley,
                    order_pid=pid,
                )

                for product_id, quantity in json.loads(trolley).items():
                    product = Product.objects.get(id=product_id)
                    order_line_item = OrderLineItem(
                        order=checkout_order,
                        product=product,
                        quantity=quantity,
                    )
                    order_line_item.save()

            except Exception as e:
                # other errors
                if checkout_order:
                    checkout_order.delete()
                return HttpResponse(
                    content=f'Webhook received {event["type"]}. ERROR {e}',
                    status=500)

        return HttpResponse(
            content=f'Webhook received {event["type"]}. \
                Order create with webhook handler',
            status=200)

    def handle_payment_failed(self, event):
        # handle a webhook payment failed event

        return HttpResponse(
            content=f'Webhook received {event["type"]}',
            status=200,
        )
