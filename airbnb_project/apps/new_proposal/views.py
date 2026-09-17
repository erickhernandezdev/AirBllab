from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import NewProposalForm
from ..core.models import (
    Accommodation,
    Service,
    Activity,
    AccommodationType,
    ActivityType,
    ServiceType,
)


@login_required
def add_new_proposal(request):
    form = NewProposalForm()

    if request.method == "POST":
        selected_type = request.POST.get("type")
        form = NewProposalForm(request.POST, request.FILES, selected_type=selected_type)

        if form.is_valid():
            host = request.user
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            proposal_type = form.cleaned_data["type"]
            location = form.cleaned_data["location"]
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            price = form.cleaned_data["price"]
            image = request.FILES.get("image")

            proposal_subtype = form.cleaned_data["subtype"]

            if proposal_type == "Alojamiento":
                proposal_subtype = AccommodationType.objects.get(name=proposal_subtype)
            elif proposal_type == "Actividad":
                proposal_subtype = ActivityType.objects.get(name=proposal_subtype)
            else:
                proposal_subtype = ServiceType.objects.get(name=proposal_subtype)

            if proposal_type == "Alojamiento":
                new_accommodation = Accommodation(
                    host=host,
                    accommodation_type=proposal_subtype,
                    name=name,
                    description=description,
                    location=location,
                    price=price,
                    available_from=start_date,
                    available_to=end_date,
                    status="Pendiente",
                    image=image,
                )
                new_accommodation.save()

            elif proposal_type == "Actividad":
                new_activity = Activity(
                    host=host,
                    activity_type=proposal_subtype,
                    name=name,
                    description=description,
                    location=location,
                    price=price,
                    status="Pendiente",
                    image=image,
                )
                new_activity.save()

            else:
                new_service = Service(
                    host=host,
                    service_type=proposal_subtype,
                    name=name,
                    description=description,
                    price=price,
                    status="Pendiente",
                    image=image,
                )
                new_service.save()

            messages.success(request, "¡Propuesta enviada con éxito!")
            return redirect("my_publications")

    return render(request, "new_proposal/new_proposal.html", {"form": form})
