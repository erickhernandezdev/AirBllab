from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.core.models import Invoice, CustomUser as User

DB_ALIAS = 'airbnb_user'

@login_required
def history_view(request):
    user = User.objects.using(DB_ALIAS).get(pk=request.user.pk)

    invoices = Invoice.objects.using(DB_ALIAS).filter(reservation__guest=user)

    context = {
        'invoices': invoices,
    }
    return render(request, 'history.html', context)
