from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem

# code taken from code institute lecture


@receiver(post_save, sender=OrderLineItem)
def update_save(sender, instance, created, **kwargs):
    """
    update order total following adding or updating lineitems
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def delete_save(sender, instance, **kwargs):
    """
    delete order total following deleting lineitems
    """
    instance.order.update_total()
