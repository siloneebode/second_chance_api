import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from Domain.order.models import Order, Transaction
from Domain.order.serializers import OrderSerializer


@receiver(post_save, sender=Order)
def create_all_for_new_user(sender, instance, **kwargs):
    transaction = Transaction(
        owner=instance.buyer,
        price=instance.price,
        method=instance.method,
        first_name=instance.first_name,
        last_name=instance.last_name,
        city=instance.city,
        phone=instance.phone,
        street=instance.street,
        fee=instance.fee,
        product=instance.product
    )
    transaction.save()

    # on prépare les emails à envoyer à chaque utilisateur.
    seller_template = render_to_string("mails/order/seller.html", {'data': OrderSerializer(instance).data}),
    client_template = render_to_string("mails/order/client.html", {'data': OrderSerializer(instance).data}),
    text_client_template = strip_tags(client_template)
    text_template = strip_tags(seller_template)


