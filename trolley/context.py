from decimal import Decimal
from django.conf import settings


def trolley_contents(request):

    trolley_items = []
    total = 0
    items_count = 0
    delivery_difference = settings.FREE_DELIVERY_MIN_SPEND - total

    if delivery_difference > 0:
        delivery_charge = Decimal(total * settings.APPLY_DELIVERY_PERCENTAGE)
    else:
        delivery_charge = 0

    free_delivery_min_spend = settings.FREE_DELIVERY_MIN_SPEND,
    grand_total = total + delivery_charge

    context = {
        'trolley_items': trolley_items,
        'total': total,
        'items_count': items_count,
        'delivery_difference': delivery_difference,
        'free_delivery_min_spend': free_delivery_min_spend,
        'delivery_charge': delivery_charge,
        'grand_total': grand_total,
    }

    return context
