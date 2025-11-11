from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import NewProposalForm
from ..core.models import Accommodation, Service, Activity, AccommodationType, ActivityType, ServiceType
from django.contrib.auth.decorators import login_required

@login_required
def add_new_proposal(request):
    form = NewProposalForm()

    if request.method == 'POST':
        selected_type = request.POST.get('type')
        form = NewProposalForm(request.POST, selected_type=selected_type)
        if form.is_valid():
            host = request.user
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            proposal_type = form.cleaned_data['type']
            location = form.cleaned_data['location']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            price = form.cleaned_data['price']

            proposal_subtype = form.cleaned_data['subtype']
            if proposal_type == 'Alojamiento':
                proposal_subtype = AccommodationType.objects.using('airbnb_user').get(name=proposal_subtype)
            elif proposal_type == 'Actividad':
                proposal_subtype = ActivityType.objects.using('airbnb_user').get(name=proposal_subtype)
            else:
                proposal_subtype = ServiceType.objects.using('airbnb_user').get(name=proposal_subtype)

            if proposal_type == 'Alojamiento':
                new_accommodation = Accommodation(
                    host=host,
                    accommodation_type=proposal_subtype,
                    name=name,
                    description=description,
                    location=location,
                    price=price,
                    available_from=start_date,
                    available_to=end_date,
                    status='Pendiente'
                )
                new_accommodation.save(using='airbnb_user')

            elif proposal_type == 'Actividad':
                new_activity = Activity(
                    host=host,
                    activity_type=proposal_subtype,
                    name=name,
                    description=description,
                    location=location,
                    price=price,
                    status='Pendiente'
                )
                new_activity.save(using='airbnb_user')

            else:
                new_service = Service(
                    host=host,
                    service_type=proposal_subtype,
                    name=name,
                    description=description,
                    price=price,
                    status='Pendiente'
                )
                new_service.save(using='airbnb_user')

            messages.success(request, "¡Propuesta enviada con éxito!")
            return redirect('my_publications')

    return render(request, 'new_proposal/new_proposal.html', {'form': form})
