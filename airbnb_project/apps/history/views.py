from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.core.models import CustomUser as User
from apps.core.models import Invoice


@login_required
def history_view(request):
    user = User.objects.get(pk=request.user.pk)

    invoices = Invoice.objects.filter(reservation__guest=user)

    context = {
        "invoices": invoices,
    }

    return render(request, "history.html", context)
