from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.dateparse import parse_date
from apps.core.models import Cart, CartActivity, CartService, Reservation, Invoice, InvoiceItem, ReservationActivity, ReservationService
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from django.utils import timezone

class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = getattr(self.request.user, 'cart', None)

        success = self.request.GET.get('success') == 'true'
        canceled = self.request.GET.get('canceled') == 'true'
        empty = self.request.GET.get('empty') == 'true'

        if success and cart:
            reservation = Reservation.objects.create(
                guest=self.request.user,
                accommodation=cart.accommodation,
                start_date=cart.start_date,
                end_date=cart.end_date,
                status="CONFIRMED"
            )

            total_accommodation = cart.price_total or 0
            services_in_cart = CartService.objects.filter(cart=cart)
            activities_in_cart = CartActivity.objects.filter(cart=cart)

            total_services = sum(float(s.total_price) for s in services_in_cart)
            total_activities = sum(float(a.total_price) for a in activities_in_cart)
            grand_total = total_accommodation + total_services + total_activities

            invoice = Invoice.objects.create(
                reservation=reservation,
                amount=grand_total,
                payment_method="Stripe",
                paid_at=timezone.now()
            )

            if cart.accommodation:
                InvoiceItem.objects.create(
                    invoice=invoice,
                    quantity=cart.nights or 1,
                    unit_price=cart.price_total or 0,
                    total=cart.price_total or 0
                )

            for s in services_in_cart:
                InvoiceItem.objects.create(
                    invoice=invoice,
                    quantity=1,
                    unit_price=s.total_price,
                    total=s.total_price
                )

                ReservationService.objects.create(
                    reservation=reservation,
                    service=s.service,
                    total_price=s.total_price,
                    date=s.date
                )

            for a in activities_in_cart:
                InvoiceItem.objects.create(
                    invoice=invoice,
                    quantity=1,
                    unit_price=a.total_price,
                    total=a.total_price
                )

                ReservationActivity.objects.create(
                    reservation=reservation,
                    activity=a.activity,
                    total_price=a.total_price,
                    date=a.date
                )

            CartService.objects.filter(cart=cart).delete()
            CartActivity.objects.filter(cart=cart).delete()

            cart.accommodation = None
            cart.start_date = None
            cart.end_date = None
            cart.nights = None
            cart.price_total = None
            cart.save()

            context['message'] = "Pago realizado con éxito."
        elif canceled:
            context['message'] = "El pago fue cancelado."
        elif empty:
            context['message'] = "No hay ítems en el carrito para pagar."

        if cart:
            activities = CartActivity.objects.filter(cart=cart)
            services = CartService.objects.filter(cart=cart)

            total_accommodation = cart.price_total or 0
            total_activities = sum(float(a.total_price) for a in activities)
            total_services = sum(float(s.total_price) for s in services)

            context.update({
                'cart': cart,
                'activities': activities,
                'services': services,
                'total_accommodation': total_accommodation,
                'total_activities': total_activities,
                'total_services': total_services,
                'grand_total': total_accommodation + total_activities + total_services,
            })

        return context

class AddToCartView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        data = request.POST
        cart, created = Cart.objects.get_or_create(user=user)

        if 'accommodation_id' in data:
            cart.accommodation_id = data.get('accommodation_id')
            cart.start_date = parse_date(data.get('start_date'))
            cart.end_date = parse_date(data.get('end_date'))
            cart.nights = int(data.get('nights', 0))
            cart.price_total = int(data.get('price_total', 0))
            cart.save()

        elif 'service_id' in data:
            CartService.objects.create(
                cart=cart,
                service_id=data.get('service_id'),
                total_price=data.get('total_price'),
                date=parse_date(data.get('date'))
            )

        elif 'activity_id' in data:
            CartActivity.objects.create(
                cart=cart,
                activity_id=data.get('activity_id'),
                total_price=data.get('total_price'),
                date=parse_date(data.get('date'))
            )

        return JsonResponse({'status': 'ok'})

class ClearCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart = getattr(request.user, 'cart', None)
        if cart:
            cart.accommodation = None
            cart.start_date = None
            cart.end_date = None
            cart.nights = None
            cart.price_total = None
            cart.save()
        return redirect('cart')

class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart = getattr(request.user, 'cart', None)
        if cart:
            cart.accommodation = None
            cart.start_date = None
            cart.end_date = None
            cart.nights = None
            cart.price_total = None
            cart.save()
        return redirect('cart')

class RemoveActivityView(LoginRequiredMixin, View):
    def post(self, request, pk):
        activity = get_object_or_404(CartActivity, pk=pk, cart=request.user.cart)
        activity.delete()
        return redirect('cart')
    
class RemoveServiceView(LoginRequiredMixin, View):
    def post(self, request, pk):
        service = get_object_or_404(CartService, pk=pk, cart=request.user.cart)
        service.delete()
        return redirect('cart')