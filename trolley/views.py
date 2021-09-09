from django.shortcuts import (
    render, redirect, get_object_or_404, reverse, HttpResponse)

from store.models import Product, Category


def view_trolley(request):
    """ A view to display the trolley"""

    return render(request, 'trolley/view_trolley.html')


def add_to_trolley(request, product_id):

    quantity = int(request.POST.get('quantity'))

    trolley = request.session.get('trolley', {})

    if product_id in list(trolley.keys()):
        trolley[product_id] += quantity
    else:
        trolley[product_id] = quantity

    request.session['trolley'] = trolley
    return redirect('view_trolley')


def update_trolley(request, product_id):
    quantity = int(request.POST.get('quantity'))
    trolley = request.session.get('trolley', {})

    if quantity > 0:
        trolley[product_id] = quantity

    else:
        trolley.pop(product_id)

    request.session['trolley'] = trolley

    return redirect(reverse('view_trolley'))


def delete_trolley_product(request, product_id):

    product = get_object_or_404(Product, pk=product_id)
    trolley = request.session.get('trolley', {})

    trolley.pop(product_id)

    request.session['trolley'] = trolley
    return redirect(reverse('view_trolley'))
