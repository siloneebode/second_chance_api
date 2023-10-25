import uuid
from datetime import timedelta

from django.db import transaction
from django.http.response import HttpResponse
from django.utils.timezone import now
from rest_framework import serializers

from Domain.additionalInfo.models import Address
from Domain.deliverySetting.models import Delivery
from Domain.order.models import Order
from Domain.paiementMethod.models import PaiementMethod
from Domain.phone.models import Phone
from Domain.product.models import Product
from Domain.wallet.models import Wallet
import http.client
import json
from django.conf import settings


def create_order(data, kwargs, request):
    # je vérifie que le produit existe et qu'il n'est pas deja vendu.
    product = Product.objects.get(is_sold=False, pk=kwargs['product'])
    if product is not None:
        seller = product.owner
        user_wallet = Wallet.objects.get(owner=request.user)
        seller_wallet = Wallet.objects.get(owner=seller)
        method = PaiementMethod.objects.get(pk=data('method'))
        delivery = Delivery.objects.get(pk=data['delivery'])
        address = Address.objects.get(pk=data['address'])
        price = product.price + delivery.price
        if data['has_verification']:
            price = price + 300
        if method and delivery and address is not None:
            x_data = {
                'delivery': delivery,
                'method': method,
                'product': product,
                'client': request.user,
                'user_wallet': user_wallet,
                'seller_wallet': seller_wallet,
                'price': price,
                'request': request,
                'address': address
            }
            return sub_paiement_module(x_data)
        else:
            raise serializers.ValidationError({"message": "Erreur inconnue veuillez ressayer..."})
    else:
        raise serializers.ValidationError({"message": "Le produit n'existe pas ou a deja été vendu.."})


def sub_paiement_module(x_data):
    if x_data['user_wallet'].price >= x_data['price']:
        # On procède au paiement sans faire appel à l'api de paiement.

        # on passe la fonction en transaction.
        with transaction.atomic():
            return pay_with_wallet(x_data)
    else:
        # On fait appel à L'API de mycool-pay
        return initiate_paiement(x_data)


def pay_with_wallet(x_data):
    # on déduit le montant du wallet.
    x_data['user_wallet'].price -= x_data['price']
    x_data['user_wallet'].save()

    # on ajoute le montant en attente dans le wallet du vendeur
    x_data['seller_wallet'].price_waiting += x_data['price']
    x_data['seller_wallet'].save()
    # Je crée la transaction au calme.

    create_order_instance(x_data)


def initiate_paiement(x_data):
    price = x_data['price'] - x_data['user_wallet']
    ref = str(uuid.uuid4())
    conn = http.client.HTTPSConnection("my-coolpay.com")
    payload = json.dumps({
        "transaction_amount": price,
        "transaction_currency": "XAF",
        "transaction_reason": "paiement",
        "app_transaction_ref": ref + '.' + x_data['product'].id + '.' + x_data['method'].id + '.' + x_data[
            'delivery'].id + '.' + x_data['address'].id + '.' + x_data['verification'],
        "customer_phone_number": x_data['request'].data['phone'],
        "customer_name": x_data['client'].username,
        "customer_email": x_data['client'].email,
        "customer_lang": x_data['client'].lang
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    try:
        conn.request("POST", '/api/' + settings.MYCOOL_PUBLIC_KEY + '/paylink', payload, headers)
        res = conn.getresponse()
        data = res.read()
        data.decode("utf-8")
    except:
        raise serializers.ValidationError({"message": "Erreur lors du paiement..."})

    response = HttpResponse(data)
    if response['status'] == 'success':
        create_order_instance(x_data)
        return response['payment_url']
    else:
        raise serializers.ValidationError({"message": "Erreur lors du paiement..."})


def create_order_instance(x_data):
    CLIENT_OK_TIME = 3
    TIME_FOR_SELLER_AFTER_ACCEPTED = 1
    ORDER_FEE = 20
    order = Order(
        ref=uuid.uuid4(),
        buyer=x_data['client'],
        price=x_data['price'],
        product=x_data['product'],
        delivery=x_data['delivery'],
        method=x_data['method'],
        first_name=x_data['address'].data['first_name'],
        last_name=x_data['address'].data['last_name'],
        street=x_data['address'].data['street'],
        city=x_data['address'].data['city'],
        has_verification=x_data['verification'],
    )

    # si le client a choisi une livraison personnalisée
    if x_data['delivery'].owner == x_data['client']:
        # on donne un délai de 3 jours pour qu'il confirme que tout est OK sinon on annule tout
        order.client_confirm_receive_expired_at = now() + timedelta(days=CLIENT_OK_TIME)
        order.fee = 20
    else:
        order.fee = 10

    order.save()
