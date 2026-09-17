import uuid
from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from apps.core.models import (
    Cart,
    CartActivity,
    CartService,
    Reservation,
    Invoice,
    InvoiceItem,
    ReservationActivity,
    ReservationService,
    Accommodation,
    Service,
    Activity,
)

User = get_user_model()


class CartView(LoginRequiredMixin, TemplateView):
    template_name = "cart/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.request.user.pk)
        cart = Cart.objects.filter(user=user).first()

        if cart:
            activities = CartActivity.objects.filter(cart=cart)
            services = CartService.objects.filter(cart=cart)

            total_accommodation = cart.price_total or 0
            total_activities = sum(float(a.total_price) for a in activities)
            total_services = sum(float(s.total_price) for s in services)

            context.update(
                {
                    "cart": cart,
                    "activities": activities,
                    "services": services,
                    "total_accommodation": total_accommodation,
                    "total_activities": total_activities,
                    "total_services": total_services,
                    "grand_total": (
                        total_accommodation + total_activities + total_services
                    ),
                }
            )

        message = self.request.GET.get("message")
        if message:
            context["message"] = message

        return context


def luhn_check(card_number):
    digits = [int(d) for d in card_number]
    checksum = 0
    parity = len(digits) % 2

    for i, d in enumerate(digits):
        if i % 2 == parity:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d

    return checksum % 10 == 0


def expiry_valid(expiry):
    try:
        month, year = expiry.split("/")
        month = int(month)
        year = int("20" + year)
        now = date.today()

        return 1 <= month <= 12 and (
            year > now.year or (year == now.year and month >= now.month)
        )
    except (ValueError, AttributeError):
        return False


@login_required
def checkout(request):
    if request.method == "POST":
        card_number = request.POST.get("card_number")
        expiry = request.POST.get("expiry")
        cvv = request.POST.get("cvv")

        if not card_number or not card_number.isdigit() or len(card_number) != 16:
            return redirect("/cart?message=Pago rechazado: número de tarjeta inválido")

        if not luhn_check(card_number):
            return redirect("/cart?message=Pago rechazado: tarjeta no válida")

        if not expiry_valid(expiry):
            return redirect("/cart?message=Pago rechazado: tarjeta vencida")

        if not cvv or not cvv.isdigit() or len(cvv) != 3 or cvv == "000":
            return redirect("/cart?message=Pago rechazado: CVV inválido")

        if not card_number.startswith("4"):
            return redirect(
                "/cart?message=El pago fue rechazado: solo se aceptan tarjetas Visa"
            )

        payment_token = str(uuid.uuid4())

        user = User.objects.get(pk=request.user.pk)
        cart = Cart.objects.filter(user=user).first()

        if cart:
            accommodation = None

            if cart.accommodation_id:
                accommodation = Accommodation.objects.get(pk=cart.accommodation_id)

            reservation = Reservation.objects.create(
                guest=user,
                accommodation=accommodation,
                start_date=cart.start_date,
                end_date=cart.end_date,
                status="CONFIRMED",
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
                payment_method=f"Card-{payment_token}",
                paid_at=timezone.now(),
            )

            if cart.accommodation:
                InvoiceItem.objects.create(
                    invoice=invoice,
                    quantity=cart.nights or 1,
                    unit_price=cart.price_total or 0,
                    total=cart.price_total or 0,
                )

            for s in services_in_cart:
                service_obj = Service.objects.get(pk=s.service_id)

                InvoiceItem.objects.create(
                    invoice=invoice,
                    quantity=1,
                    unit_price=s.total_price,
                    total=s.total_price,
                )

                ReservationService.objects.create(
                    reservation=reservation,
                    service=service_obj,
                    total_price=s.total_price,
                    date=s.date,
                )

            for a in activities_in_cart:
                activity_obj = Activity.objects.get(pk=a.activity_id)

                InvoiceItem.objects.create(
                    invoice=invoice,
                    quantity=1,
                    unit_price=a.total_price,
                    total=a.total_price,
                )

                ReservationActivity.objects.create(
                    reservation=reservation,
                    activity=activity_obj,
                    total_price=a.total_price,
                    date=a.date,
                )

            services_in_cart.delete()
            activities_in_cart.delete()

            cart.accommodation = None
            cart.start_date = None
            cart.end_date = None
            cart.nights = None
            cart.price_total = None
            cart.save()

        return redirect(
            f"/cart?message=Pago realizado con éxito. Código: {payment_token}"
        )


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request):
        user = User.objects.get(pk=request.user.pk)
        data = request.POST

        cart, created = Cart.objects.get_or_create(user=user)

        if "accommodation_id" in data:
            if cart.accommodation_id:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Ya tienes un alojamiento en tu carrito",
                    }
                )

            cart.accommodation_id = data.get("accommodation_id")
            cart.start_date = parse_date(data.get("start_date"))
            cart.end_date = parse_date(data.get("end_date"))
            cart.nights = int(data.get("nights", 0))
            cart.price_total = int(data.get("price_total", 0))
            cart.save()

        elif "service_id" in data:
            service_id = data.get("service_id")

            exists = CartService.objects.filter(
                cart=cart, service_id=service_id
            ).exists()

            if exists:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Este servicio ya está en tu carrito",
                    }
                )

            CartService.objects.create(
                cart=cart,
                service_id=service_id,
                total_price=data.get("total_price"),
                date=parse_date(data.get("date")),
            )

        elif "activity_id" in data:
            activity_id = data.get("activity_id")

            exists = CartActivity.objects.filter(
                cart=cart, activity_id=activity_id
            ).exists()

            if exists:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Esta actividad ya está en tu carrito",
                    }
                )

            CartActivity.objects.create(
                cart=cart,
                activity_id=activity_id,
                total_price=data.get("total_price"),
                date=parse_date(data.get("date")),
            )

        return JsonResponse({"status": "success", "message": "Agregado al carrito"})


class ClearCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.pk)
        cart = Cart.objects.filter(user=user).first()

        if cart:
            CartActivity.objects.filter(cart=cart).delete()
            CartService.objects.filter(cart=cart).delete()

            cart.accommodation = None
            cart.start_date = None
            cart.end_date = None
            cart.nights = None
            cart.price_total = None
            cart.save()

        return redirect("cart")


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.pk)
        cart = Cart.objects.filter(user=user).first()

        if cart:
            cart.accommodation = None
            cart.start_date = None
            cart.end_date = None
            cart.nights = None
            cart.price_total = None
            cart.save()

        return redirect("cart")


class RemoveActivityView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = User.objects.get(pk=request.user.pk)
        cart = Cart.objects.filter(user=user).first()

        activity = get_object_or_404(CartActivity, pk=pk, cart=cart)

        activity.delete()

        return redirect("cart")


class RemoveServiceView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = User.objects.get(pk=request.user.pk)
        cart = Cart.objects.filter(user=user).first()

        service = get_object_or_404(CartService, pk=pk, cart=cart)

        service.delete()

        return redirect("cart")
