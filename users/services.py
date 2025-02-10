import requests
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET


def create_product(name, description="Оплата курса"):
    try:
        product = stripe.Product.create(name=name, description=description)
        return product['id']
    except Exception as e:
        return {'error': str(e)}


def create_price(product_id, amount):
    try:
        unit_amount = int(float(amount) * 100)
        price = stripe.Price.create(
            unit_amount=unit_amount,
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
