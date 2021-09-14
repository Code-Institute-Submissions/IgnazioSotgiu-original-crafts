from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.conf import settings
from store.models import Product


def trolley_contents(request):

    trolley_items = []
    total = 0
    items_count = 0
    line_product_subtotal = 0

    trolley = request.session.get('trolley', {})
    for product_id, quantity in trolley.items():
        product = get_object_or_404(Product, pk=product_id)

        if product.special_price:
            total += product.special_price * quantity
            line_product_subtotal = product.special_price * quantity
        else:
            total += product.price * quantity
            line_product_subtotal = product.price * quantity
        items_count += quantity
        trolley_items.append({
            'product_id': product_id,
            'product': product,
            'total': round(total, 2),
            'quantity': quantity,
            'items_count': items_count,
            'line_product_subtotal': round(line_product_subtotal, 2),
        })

    delivery_difference = settings.FREE_DELIVERY_MIN_SPEND - total

    if delivery_difference > 0:
        delivery_charge = Decimal(
            total * settings.APPLY_DELIVERY_PERCENTAGE / 100)
    else:
        delivery_charge = 0

    free_delivery_min_spend = settings.FREE_DELIVERY_MIN_SPEND
    grand_total = total + delivery_charge

    context = {
        'trolley_items': trolley_items,
        'total': round(total, 2),
        'items_count': items_count,
        'delivery_difference': round(delivery_difference, 2),
        'free_delivery_min_spend': free_delivery_min_spend,
        'delivery_charge': round(delivery_charge, 2),
        'grand_total': round(grand_total, 2),
    }

    return context
