from django.shortcuts import (
    render, redirect, get_object_or_404, reverse, HttpResponse)
from django.contrib import messages
from .forms import CheckoutForm
from store.models import Product, Category


def view_checkout_page(request):
    """ A view to display the checkout page"""
    trolley = request.session.get('trolley', {})
    if not trolley:
        messages.info(request, 'Your trolley is empty! Go Shopping')
        return redirect('products')

    form = CheckoutForm()
    if request.method == 'POST':
        form_data = {
            'deliver_to_name': request.POST['deliver_to_name'],
            'email_address': request.POST['email_address'],
            'street_address': request.POST['street_address'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'country': request.POST['country'],
            'zip_postcode': request.POST['zip_postcode'],
        }
        order_form = CheckoutForm(form_data)
        if order_form.is_valid():
            messages.success(request, 'the form is valid')
    template = 'checkout/checkout_page.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
