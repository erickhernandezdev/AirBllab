from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Property, Activity
from apps.core.models import Accommodations, Activities as CoreActivities, Services

@login_required
def approved_items_list(request):
    """Vista pública para usuarios normales - muestra solo items aprobados"""
    
    # Propiedades y actividades del sistema principal (aprobadas)
    approved_properties = Property.objects.filter(is_approved=True)
    approved_activities = Activity.objects.filter(is_approved=True)
    
    # Elementos aprobados en el nuevo sistema (status='Aprobado')
    approved_accomodations = Accommodations.objects.filter(status='Aprobado')
    approved_proposal_activities = CoreActivities.objects.filter(status='Aprobado')
    approved_services = Services.objects.filter(status='Aprobado')
    
    context = {
        'properties': approved_properties,
        'activities': approved_activities,
        'accomodations': approved_accomodations,
        'proposal_activities': approved_proposal_activities,
        'services': approved_services,
    }
    
    return render(request, 'properties/approved_items.html', context)
