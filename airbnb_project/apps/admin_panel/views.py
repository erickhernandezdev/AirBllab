from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from apps.properties.models import Property, Activity
from apps.users.models import CustomUser
from apps.core.models import Accommodations, Activities as CoreActivities, Services
from .models import ApprovalLog

def admin_required(view_func):
  """Decorator para verificar que el usuario es administrador"""
  def _wrapped_view(request, *args, **kwargs):
    if not request.user.is_authenticated or request.user.role != 'ADMIN':
      messages.error(request, "No tienes permisos para acceder a esta sección.")
      return redirect('home')
    return view_func(request, *args, **kwargs)
  return _wrapped_view

@admin_required
def admin_dashboard(request):
  """Dashboard principal del administrador"""
  # Estadísticas
  stats = {
    'total_users': CustomUser.objects.count(),
    'total_properties': Property.objects.count(),
    'total_activities': Activity.objects.count(),
    'pending_properties': Property.objects.filter(is_approved=False).count(),
    'pending_activities': Activity.objects.filter(is_approved=False).count(),
    # Propuestas nuevas
  'pending_accomodations': Accommodations.objects.filter(Q(status='pending') | Q(status='Pendiente')).count(),
  'pending_proposal_activities': CoreActivities.objects.filter(Q(status='pending') | Q(status='Pendiente')).count(),
  'pending_services': Services.objects.filter(Q(status='pending') | Q(status='Pendiente')).count(),
    'recent_approvals': ApprovalLog.objects.order_by('-created_at')[:5]
  }
  
  return render(request, 'admin_panel/dashboard.html', {'stats': stats})

@admin_required
def pending_approval_list(request):
  """Lista de propiedades y actividades pendientes de aprobación"""
  pending_properties = Property.objects.filter(is_approved=False)
  pending_activities = Activity.objects.filter(is_approved=False)
  
  # Propuestas del módulo new_proposal
  pending_accomodations = Accommodations.objects.filter(Q(status='pending') | Q(status='Pendiente'))
  pending_proposal_activities = CoreActivities.objects.filter(Q(status='pending') | Q(status='Pendiente'))
  pending_services = Services.objects.filter(Q(status='pending') | Q(status='Pendiente'))
  
  context = {
    'pending_properties': pending_properties,
    'pending_activities': pending_activities,
    'pending_accomodations': pending_accomodations,
    'pending_proposal_activities': pending_proposal_activities,
    'pending_services': pending_services,
  }

  return render(request, 'admin_panel/pending_approval.html', context)

@admin_required
def approval_detail(request, item_type, item_id):
  """Detalle de un item para aprobación/rechazo"""
  if item_type == 'property':
    item = get_object_or_404(Property, id=item_id)
    template = 'admin_panel/approval_detail.html'
  elif item_type == 'activity':
    item = get_object_or_404(Activity, id=item_id)
    template = 'admin_panel/approval_detail.html'
  else:
    messages.error(request, "Tipo de ítem inválido.")
    return redirect('admin_pending_approval')

  # Obetener historial de aprobaciones
  approval_logs = ApprovalLog.objects.filter(
    Q(property=item) if item_type == 'property' else Q(activity=item)
  ).order_by('-created_at')

  context = {
    'item' : item,
    'item_type': item_type,
    'approval_logs': approval_logs
  }

  return render(request, template, context)

@admin_required
def approve_item(request, item_type, item_id):
  """Aprobar un item (propiedad o actividad)"""
  if request.method == 'POST':
    if item_type == 'property':
      item = get_object_or_404(Property, id=item_id)
    elif item_type == 'activity':
      item = get_object_or_404(Activity, id=item_id)
    else:
      messages.error(request, "Tipo de ítem inválido.")
      return redirect('admin_pending_approval')
    
    # Aprobar el item
    item.is_approved = True
    item.approved_by = request.user
    item.approved_at = timezone.now()
    item.save()

    # Crear registro en el log
    approval_data = {
      'admin_user': request.user,
      'status': 'approved',
      'notes': request.POST.get('notes', '')
    }

    if item_type == 'property':
      approval_data['property'] = item
    else:
      approval_data['activity'] = item

    ApprovalLog.objects.create(**approval_data)

    messages.success(request, f"{item_type.capitalize()} aprobado exitosamente!")
    return redirect('admin_pending_approval')
  
  return redirect('admin_pending_approval')

@admin_required
def reject_item(request, item_type, item_id):
  """Rechazar un item (propiedad o actividad)"""
  if request.method == 'POST':
    if item_type == 'property':
      item = get_object_or_404(Property, id=item_id)
    elif item_type == 'activity':
      item = get_object_or_404(Activity, id=item_id)
    else:
      messages.error(request, "Tipo de ítem inválido.")
      return redirect('admin_pending_approval')
    
    notes = request.POST.get('notes', 'Razón no especificada')

    # Crear registro en el log antes de eliminar
    approval_data = {
      'admin_user': request.user,
      'status': 'rejected',
      'notes': notes
    }

    if item_type == 'property':
      approval_data['property'] = item
    else:
      approval_data['activity'] = item

    ApprovalLog.objects.create(**approval_data)

    item_name = item.name
    item.delete()

    messages.warning(request, f"{item_type.capitalize()} '{item_name}' rechazado y eliminado.")
    return redirect('admin_pending_approval')
  
  return redirect('admin_pending_approval')

@admin_required
def user_list(request):
  """Lista de todos los usuarios registrados"""
  users = CustomUser.objects.all().order_by('-date_joined')

  # Estadísticas de usuarios
  user_stats = {
    'total': users.count(),
    'admins': users.filter(role='ADMIN').count(),
    'regular_users': users.filter(role='USER').count(),
    'active_today': users.filter(last_login__date=timezone.now().date()).count()
  }

  context = {
    'users': users,
    'user_stats': user_stats
  }

  return render(request, 'admin_panel/user_list.html', context)

@admin_required
def proposal_detail(request, item_type, item_id):
  """Detalle de una propuesta para aprobación/rechazo"""
  if item_type == 'accomodation':
    item = get_object_or_404(Accommodations, id=item_id)
  elif item_type == 'proposal_activity':
    item = get_object_or_404(CoreActivities, id=item_id)
  elif item_type == 'service':
    item = get_object_or_404(Services, id=item_id)
  else:
    messages.error(request, "Tipo de propuesta inválido.")
    return redirect('admin_panel:admin_pending_approval')

  context = {
    'item': item,
    'item_type': item_type,
  }

  return render(request, 'admin_panel/proposal_detail.html', context)

@admin_required
def approve_proposal(request, item_type, item_id):
  """Aprobar una propuesta (alojamiento, actividad o servicio)"""
  if request.method == 'POST':
    if item_type == 'accomodation':
      item = get_object_or_404(Accommodations, id=item_id)
    elif item_type == 'proposal_activity':
      item = get_object_or_404(CoreActivities, id=item_id)
    elif item_type == 'service':
      item = get_object_or_404(Services, id=item_id)
    else:
      messages.error(request, "Tipo de propuesta inválido.")
      return redirect('admin_panel:admin_pending_approval')
    
    # Cambiar estado a aprobado
    item.status = 'Aprobado'
    item.save()

    # Crear registro en el log (placeholder para auditoría futura)
    notes = request.POST.get('notes', f'Propuesta de {item_type} aprobada')
    
    messages.success(request, f"¡Propuesta '{item.name}' aprobada exitosamente!")
    return redirect('admin_panel:admin_pending_approval')
  
  return redirect('admin_panel:admin_pending_approval')

@admin_required
def reject_proposal(request, item_type, item_id):
  """Rechazar una propuesta (alojamiento, actividad o servicio)"""
  if request.method == 'POST':
    if item_type == 'accomodation':
      item = get_object_or_404(Accommodations, id=item_id)
    elif item_type == 'proposal_activity':
      item = get_object_or_404(CoreActivities, id=item_id)
    elif item_type == 'service':
      item = get_object_or_404(Services, id=item_id)
    else:
      messages.error(request, "Tipo de propuesta inválido.")
      return redirect('admin_panel:admin_pending_approval')
    
    notes = request.POST.get('notes', 'Razón no especificada')
    
    # Cambiar estado a rechazado (mantener el registro)
    item.status = 'Rechazado'
    item.save()

    messages.warning(request, f"Propuesta '{item.name}' rechazada.")
    return redirect('admin_panel:admin_pending_approval')
  
  return redirect('admin_panel:admin_pending_approval')
