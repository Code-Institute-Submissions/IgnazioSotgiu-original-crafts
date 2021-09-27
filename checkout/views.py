from django.shortcuts import (
    render, redirect, get_object_or_404, reverse,
    HttpResponse)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from .forms import CheckoutForm
from profiles.forms import ProfileForm
from store.models import Product
from profiles.models import Profile
from trolley.context import trolley_contents
from checkout.models import CheckoutOrder, OrderLineItem
import stripe
import json

# code taken from cade institute lecture


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'save_address_details': request.POST.get('save_address_details'),
            'trolley': json.dumps(request.session.get('trolley', {})),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, (
            'There was a problem processing your order. Try again later'))
        return HttpResponse(content=e, status=400)


def view_checkout_page(request):
    """display the checkout page"""

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        trolley = request.session.get('trolley', {})
        form_info = {
            'full_name': request.POST['full_name'],
            'email_address': request.POST['email_address'],
            'phone_number': request.POST['phone_number'],
            'street_address': request.POST['street_address'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'country': request.POST['country'],
            'zip_postcode': request.POST['zip_postcode'],
        }

        checkout_form = CheckoutForm(form_info)
        if checkout_form.is_valid():
            order = checkout_form.save()
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.pid = pid
            order.order_trolley = json.dumps(trolley)
            user = request.user
            if user.is_authenticated:
                order.profile = get_object_or_404(Profile, user=request.user)
            order.save()
            for product_id, quantity in trolley.items():
                product = Product.objects.get(id=product_id)
                order_line_item = OrderLineItem(
                    order=order,
                    product=product,
                    quantity=quantity,
                )
                order_line_item.save()

            request.session['save_address_details'] = 'save-address-details' in request.POST
            return redirect(reverse(
                'checkout_completed', args=[order.order_number]),)

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
    user = request.user
    if user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)

    form = CheckoutForm(instance=profile)

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

    profile = Profile.objects.get(user=request.user)
    save_address_details = request.session.get('save_address_details')
    print(save_address_details)
    if save_address_details:
        updated_profile_address = {
            'phone_number': order.phone_number,
            'street_address': order.street_address,
            'town_or_city': order.town_or_city,
            'county': order.county,
            'country': order.country,
            'zip_postcode': order.zip_postcode,
        }
        profile_form = ProfileForm(updated_profile_address, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(
                request, 'Your Address info were successfully updated')

    # Update number in stock after products are successfully purchased
    trolley = request.session.get('trolley', {})

    for product_id, quantity in trolley.items():
        product = Product.objects.get(id=product_id)
        product.number_in_stock -= quantity
        product.save()
    context = {
        'order': order,
    }
    messages.success(request, f'Your order number {order_number} \
        was completed successfully')

    if 'trolley' in request.session:
        del request.session['trolley']

    return render(request, template, context)
