import requests
import stripe
from stripe.http_client import RequestsClient
from django.conf import settings

stripe.api_key = 'sk_test_51QpUY6Q6akmNPxzpeJkc0fcJ5rvTDiSZX8SR5cAbdsdttLYfPYkVMU3M2XC8RKTkRDnFSDZej6vnZQZPboksy72300d5kfKb4f'
    # settings.STRIPE_SECRET)


def create_product(name, description="Оплата курса"):
    try:
        product = stripe.Product.create(name=name, description=description)
        return product['id']
    except Exception as e:
        return {'error': str(e)}


def create_price(product_id, amount):
    try:
        price = stripe.Price.create(
            unit_amount=amount,
            currency="rub",
            product=product_id,
        )
        return price['id']
    except Exception as e:
        return {'error': str(e)}


def create_checkout_session(price_id, success_url, cancel_url):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session['url']
    except Exception as e:
        return {'error': str(e)}


def retrieve_session_status(session_id):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session['payment_status']
    except Exception as e:
        return {'error': str(e)}
