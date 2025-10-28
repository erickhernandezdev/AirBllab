import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse

from apps.core.models import (
    Cart, CartService, CartActivity,
    Accommodation, Service, Activity
)

def payment(request):
  return render(request, 'payment/payment.html')

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        YOUR_DOMAIN = "http://127.0.0.1:8000"

        user = request.user 
        line_items = []

        accommodations_in_cart = Cart.objects.filter(user=user)
        for cart_item in accommodations_in_cart:
            accommodation = cart_item.accommodation
            if accommodation:
                line_items.append({
                    'price_data': {
                        'currency': 'crc',
                        'unit_amount': int(accommodation.price * 100),
                        'product_data': {
                            'name': f"Alojamiento: {accommodation.name}",
                        },
                    },
                    'quantity': 1,
                })

        services_in_cart = CartService.objects.filter(cart__user=user)
        for cart_service in services_in_cart:
            service = cart_service.service
            if service:
                line_items.append({
                    'price_data': {
                        'currency': 'crc',
                        'unit_amount': int(service.price * 100),
                        'product_data': {
                            'name': f"Servicio: {service.name}",
                        },
                    },
                    'quantity': 1,
                })

        activities_in_cart = CartActivity.objects.filter(cart__user=user)
        for cart_activity in activities_in_cart:
            activity = cart_activity.activity
            if activity:
                line_items.append({
                    'price_data': {
                        'currency': 'crc',
                        'unit_amount': int(activity.price * 100),
                        'product_data': {
                            'name': f"Actividad: {activity.name}",
                        },
                    },
                    'quantity': 1,
                })

        #TODO: cambiar los urls a los del carrito
        if not line_items:
            return redirect(YOUR_DOMAIN + '/payment/')

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=YOUR_DOMAIN + '/payment/',
            cancel_url=YOUR_DOMAIN + '/homepage/',
        )

        return redirect(checkout_session.url, code=303)
