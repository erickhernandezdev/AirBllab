import stripe
import json
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.core.models import (
    Cart, CartService, CartActivity
)

class CreateCheckoutSessionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        YOUR_DOMAIN = "http://127.0.0.1:8000"

        user = request.user 
        line_items = []

        cart = Cart.objects.filter(user=user).first()
        if cart and cart.accommodation:
            line_items.append({
                'price_data': {
                    'currency': 'crc',
                    'unit_amount': int(cart.price_total * 100),
                    'product_data': {
                        'name': f"Alojamiento: {cart.accommodation.name}",
                    },
                },
                'quantity': 1,
            })

        services_in_cart = CartService.objects.using('airbnb_user').filter(cart__user=user)
        for cart_service in services_in_cart:
            if cart_service.service:
                line_items.append({
                    'price_data': {
                        'currency': 'crc',
                        'unit_amount': int(cart_service.total_price * 100),
                        'product_data': {
                            'name': f"Servicio: {cart_service.service.name}",
                        },
                    },
                    'quantity': 1,
                })

        activities_in_cart = CartActivity.objects.using('airbnb_user').filter(cart__user=user)
        for cart_activity in activities_in_cart:
            if cart_activity.activity:
                line_items.append({
                    'price_data': {
                        'currency': 'crc',
                        'unit_amount': int(cart_activity.total_price * 100),
                        'product_data': {
                            'name': f"Actividad: {cart_activity.activity.name}",
                        },
                    },
                    'quantity': 1,
                })

        if not line_items:
            return redirect(YOUR_DOMAIN + '/cart/?empty=true')

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=YOUR_DOMAIN + '/cart/?success=true',
            cancel_url=YOUR_DOMAIN + '/cart/?canceled=true',
            client_reference_id=str(user.pk),
        )

        return redirect(checkout_session.url, code=303)
