import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse

def payment(request):
  return render(request, 'payment/payment.html')

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            #TODO: Obtener los articulos del carrito de compras
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 2000,  # $20.00
                        'product_data': {
                            'name': 'Reserva de alojamiento',
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            #TODO: Redirigir al carrito
            success_url=YOUR_DOMAIN + '/payment/',
            cancel_url=YOUR_DOMAIN + '/payment/',
        )
        return redirect(checkout_session.url, code=303)
