from django.http import HttpResponse
from .models import CheckoutOrder, OrderLineItem
from store.models import Product
from django.conf import settings
from django.core.mail import send_mail
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
        billing_details = intent.charges.data[0].billing_details
        email_sent = False

        checkout_order_exists = False
        checkout_order = None
        attempt = 1
        # check if order exists in database
        while attempt <= 5:
            try:
                checkout_order = CheckoutOrder.objects.get(
                    full_name__iexact=billing_details.name,
                    email_address__iexact=billing_details.email,
                    phone_number__iexact=billing_details.phone,
                    street_address__iexact=billing_details.address.line1,
                    town_or_city__iexact=billing_details.address.city,
                    county__iexact=billing_details.address.state,
                    zip_postcode__iexact=billing_details.address.postal_code,
                    country__iexact=billing_details.address.country,
                    order_trolley=trolley,
                    order_pid=pid,
                    email_sent=email_sent,
                )

                checkout_order_exists = True
                break

            except CheckoutOrder.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if checkout_order_exists:
            # check email_sent value
            if checkout_order.email_sent:

                return HttpResponse(
                    content=f'Webhook received {event["type"]}.\
                        Found order in the database. A confirmation email\
                        was successfully sent\
                        to {checkout_order.email_address}',
                    status=200,
                )
            else:
                # send a confirmation email and set the
                # variable to true in case of success
                try:
                    checkout_order.email_sent = True
                    checkout_order.save()
                    from_email = settings.DEFAULT_FROM_EMAIL
                    recipient_list = checkout_order.email_address
                    email_subject = f'Order\
                        Confirmation { checkout_order.order_number}'
                    message = f'Thank you { checkout_order.full_name }.\
                        Your order number { checkout_order.order_number }\
                            was sucessfully completed. Thank you.\
                            If you need any help please contact us\
                            at { settings.DEFAULT_FROM_EMAIL }'

                    send_mail(email_subject, message, from_email, [
                        recipient_list], fail_silently=False)

                    return HttpResponse(
                        content=f'Webhook received {event["type"]}.\
                            Found order in the database. A confirmation email\
                            was successfully sent with webhook\
                            to {checkout_order.email_address}',
                        status=200,
                    )

                except Exception as e:

                    return HttpResponse(
                        content=f'Webhook received\
                            {event["type"]}. ERROR {e}',
                        status=500)

        else:
            checkout_order = None
            # retrieve data order from webhook and save it
            try:
                checkout_order = CheckoutOrder.objects.create(
                    full_name=billing_details.name,
                    email_address=billing_details.email,
                    phone_number=billing_details.phone,
                    street_address=billing_details.address.line1,
                    town_or_city=billing_details.address.city,
                    county=billing_details.address.state,
                    zip_postcode=billing_details.address.postal_code,
                    country=billing_details.address.country,
                    order_trolley=trolley,
                    order_pid=pid,
                    email_sent=email_sent,
                )

                for product_id, quantity in json.loads(trolley).items():
                    product = Product.objects.get(id=product_id)
                    order_line_item = OrderLineItem(
                        order=checkout_order,
                        product=product,
                        quantity=quantity,
                    )
                    order_line_item.save()

                if checkout_order.email_sent:
                    return HttpResponse(
                        content=f'Webhook received {event["type"]}.\
                            A confirmation email\
                            was successfully sent\
                            to {checkout_order.email_address}',
                        status=200,
                    )

                else:
                    try:
                        # send the confirmation email
                        checkout_order.email_sent = True
                        checkout_order.save()
                        from_email = settings.DEFAULT_FROM_EMAIL
                        recipient_list = checkout_order.email_address
                        email_subject = f'Order\
                            Confirmation { checkout_order.order_number}'
                        message = f'Thank you { checkout_order.full_name }.\
                            Your order number { checkout_order.order_number }\
                                was sucessfully completed. Thank you.\
                                If you need any help please contact us\
                                at { settings.DEFAULT_FROM_EMAIL }'

                        send_mail(email_subject, message, from_email, [
                            recipient_list], fail_silently=False)

                        return HttpResponse(
                            content=f'Webhook received {event["type"]}.\
                                Found order in the database.\
                                A confirmation email\
                                was successfully sent\
                                to {checkout_order.email_address}',
                            status=200,
                        )

                    except Exception as e:
                        # handle generic error
                        return HttpResponse(
                            content=f'Webhook received\
                                {event["type"]}. ERROR {e}',
                            status=500)

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
