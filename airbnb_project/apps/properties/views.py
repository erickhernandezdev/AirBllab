from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Property, Activity
from apps.new_proposal.models import Accomodations, Activities as ProposalActivities, Services

@login_required
def approved_items_list(request):
    """Vista pública para usuarios normales - muestra solo items aprobados"""
    
    # Propiedades y actividades del sistema principal (aprobadas)
    approved_properties = Property.objects.filter(is_approved=True)
    approved_activities = Activity.objects.filter(is_approved=True)
    
    # Propuestas aprobadas (status='active')
    approved_accomodations = Accomodations.objects.filter(status='active')
    approved_proposal_activities = ProposalActivities.objects.filter(status='active')
    approved_services = Services.objects.filter(status='active')
    
    context = {
        'properties': approved_properties,
        'activities': approved_activities,
        'accomodations': approved_accomodations,
        'proposal_activities': approved_proposal_activities,
        'services': approved_services,
    }
    
    return render(request, 'properties/approved_items.html', context)
