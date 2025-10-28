from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import NewProposalForm
from ..core.models import Accommodation, Service, Activity, AccommodationType, ActivityType, ServiceType
from django.contrib.auth.decorators import login_required

@login_required
def add_new_proposal(request):
    form = NewProposalForm()

    if request.method == 'POST':
        form = NewProposalForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            proposal_type = form.cleaned_data['type']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            price = form.cleaned_data['price']

            if proposal_type == 'Alojamiento':
                accommodation_type = AccommodationType.objects.get(name='Alojamiento')
                new_accommodation = Accommodation(
                    host=1,
                    Accommodation_type=accommodation_type,
                    name=name,
                    description=description,
                    location='Sin ubicación',
                    price_per_night=price,
                    available_from=start_date,
                    available_to=end_date,
                    status='Pendiente'
                )
                new_accommodation.save()

            elif proposal_type == 'Actividad':
                activity_type = ActivityType.objects.get(name='Actividad')
                new_activity = Activity(
                    host=1,
                    activity_type=activity_type,
                    name=name,
                    description=description,
                    location='Sin ubicación',
                    unity_price=price,
                    status='Pendiente'
                )
                new_activity.save()

            else:
                service_type = ServiceType.objects.get(name='Servicio')
                new_service = Service(
                    service_type=service_type,
                    name=name,
                    description=description,
                    price=price,
                    status='Pendiente'
                )
                new_service.save()

            messages.success(request, "¡Propuesta enviada con éxito!")
            return redirect('my_publications')

    return render(request, 'new_proposal/new_proposal.html', {'form': form})
