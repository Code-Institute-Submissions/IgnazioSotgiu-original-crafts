from django.shortcuts import (
    render, redirect, get_object_or_404,
    HttpResponseRedirect)
from django.contrib import messages
from store.models import Product


def view_trolley(request):
    """
    A view to display the trolley
    """

    return render(request, 'trolley/view_trolley.html')


def add_to_trolley(request, product_id):
    """
    A view to add products in the trolley
    """
    quantity = int(request.POST.get('quantity'))
    product = get_object_or_404(Product, id=product_id)
    trolley = request.session.get('trolley', {})

    if product_id in list(trolley.keys()):
        trolley[product_id] += quantity
    else:
        trolley[product_id] = quantity

    request.session['trolley'] = trolley
    messages.success(request, f'{product.name} has been\
        successfully added to your trolley')

    return redirect('view_trolley')


def update_trolley(request, product_id):
    """
    A view to update products in the trolley
    """
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity'))
    next = request.POST.get('next')

    trolley = request.session.get('trolley', {})

    if quantity > 0:
        trolley[product_id] = quantity
        messages.success(
            request, f'Quantity {product.name} updated successfully!')

    else:
        trolley.pop(product_id)
        messages.success(
            request, f'{product.name} removed successfully from your trolley')

    request.session['trolley'] = trolley

    return HttpResponseRedirect(next)


def delete_trolley_product(request, product_id):
    """
    A view to delete products in the trolley
    """
    product = get_object_or_404(Product, pk=product_id)
    trolley = request.session.get('trolley', {})
    next = request.POST.get('next')

    trolley.pop(product_id)
    messages.success(
            request, f'{product.name} removed successfully from your trolley')

    request.session['trolley'] = trolley
    return HttpResponseRedirect(next)
