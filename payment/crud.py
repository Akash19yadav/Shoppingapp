import stripe
from config import settings


# This is predefined method for stripe which will take total price and redirects to the suitable urls
def payment_process(total_price):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': "Your Bills"
                },
                'unit_amount_decimal': "{:.2f}".format(total_price * 100)
            },
            'quantity': 1
        }],
        mode='payment',
        success_url=settings.base_url + '/payment/done',
        cancel_url=settings.base_url + '/payment/canceled'
    )

    return session
