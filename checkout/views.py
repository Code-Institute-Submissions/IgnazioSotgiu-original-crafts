from django.shortcuts import (
    render, redirect, get_object_or_404, reverse, HttpResponse)
from django.contrib import messages
from django.conf import settings
from django.template import RequestContext
from .forms import CheckoutForm
from store.models import Product, Category
from trolley.context import trolley_contents
from checkout.models import CheckoutOrder
import stripe
import json


def view_checkout_page(request):
    """display the checkout page"""

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        trolley = request.session.get('trolley', {})
        form_info = {
            'full_name': request.POST['full_name'],
            'email_address': request.POST['email_address'],
            'street_address': request.POST['street_address'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'country': request.POST['country'],
            'zip_postcode': request.POST['zip_postcode'],
        }

        checkout_form = CheckoutForm(form_info)
        if checkout_form.is_valid():
            order = checkout_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.your_trolley = json.dumps(trolley)
            order.save()

            # for item_id in trolley.items():
            #     try:
            #         product = Product.objects.get(product_id=item_id)
            #         quantity = trolley.product.quantity

            #     except Product.DoesNotExist:
            #         messages.error(request, f'{product.name} was not\
            #             found in the database. Order NOT completed')
            #     order.delete()
            #     return redirect(reverse('view_trolley'))

            return redirect(reverse(
                'checkout_completed', args=[order.order_number]))

        else:
            messages.error(request, 'Form NOT valid.\
                 there was a problenm with your checkout form')
            return redirect(reverse('view_trolley'))

    else:
        trolley = request.session.get('trolley', {})
        if not trolley:
            messages.info(request, 'Your trolley is empty! Go Shopping')
            return redirect('products')

        your_trolley = trolley_contents(request)
        grand_total = your_trolley['grand_total']
        stripe_grand_total = round(grand_total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_grand_total,
            currency=settings.STRIPE_CURRENCY,
        )
        print(intent)

    form = CheckoutForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
             Did you forget to set it in your environment?')

    template = 'checkout/checkout_page.html'
    context = {
        'form': form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_completed(request, order_number):
    template = 'checkout/checkout_completed.html'
    order = get_object_or_404(CheckoutOrder, order_number=order_number)
    context = {
        order: order,
    }
    return render(request, template, context)