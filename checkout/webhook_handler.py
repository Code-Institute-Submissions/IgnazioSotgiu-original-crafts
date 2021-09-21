from django.http import HttpResponse
from .models import CheckoutOrder, OrderLineItem
from store.models import Product
import json

# code structure taken from code institute lecture


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
        intent = event.data.object
        pid = intent.id
        trolley = intent.metadata.trolley
        save_address_details = intent.metadata.save_address_details

        billing_details = intent.charges.data[0].billing_details
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        try:
            order_exists = False

            order = CheckoutOrder.objects.get(
                full_name__iexact=intent.charges.data[
                    0].name,
                email_address__iexact=intent.charges.data[
                    0].email,
                street_address__iexact=intent.charges.data[
                    0].billing_details.address.line1,
                town_or_city__iexact=intent.charges.data[
                    0].billing_details.address.city,
                county__iexact=intent.charges.data[
                    0].billing_details.address.state,
                zip_postcode__iexact=intent.charges.data[
                    0].billing_details.address.postal_code,
                country__iexact=intent.charges.data[
                    0].billing_details.address.country,
            )

            order_exists = True

            print(intent)
            return HttpResponse(
                content=f'Webhook received {event["type"]}.\
                    The order is alerady in the database',
                status=200,
            )
        except CheckoutOrder.DoesNotExist:
            try:
                order = CheckoutOrder.objects.create(
                    full_name=intent.charges.data[0].name,
                    email_address=intent.charges.data[0].email,
                    street_address=intent.charges.data[
                        0].billing_details.address.line1,
                    town_or_city=intent.charges.data[
                        0].billing_details.address.city,
                    county=intent.charges.data[
                        0].billing_details.address.state,
                    zip_postcode=intent.charges.data[
                        0].billing_details.address.postal_code,
                    country=intent.charges.data[
                        0].billing_details.address.country,
                )
                for product_id, quantity in json.load(trolley).items():
                    product = Product.objects.get(id=product_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()

                return HttpResponse(
                    content=f'Webhook received {event["type"]}. ERROR {e}',
                    status=500)

        return HttpResponse(
            content=f'Webhook received {event["type"]}.',
            status=200)

    def handle_payment_failed(self, event):
        # handle a webhook payment failed event

        return HttpResponse(
            content=f'Webhook received {event["type"]}',
            status=200,
        )
