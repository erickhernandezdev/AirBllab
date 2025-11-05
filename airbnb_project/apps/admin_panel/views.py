from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from apps.core.models import Accommodation, Activity, Service, CustomUser
from multifactor.decorators import multifactor_protected
from .models import ApprovalLog

def admin_required(view_func):
  """Decorator para verificar que el usuario es administrador"""
  def _wrapped_view(request, *args, **kwargs):
    if not request.user.is_authenticated or request.user.role != 'ADMIN':
      messages.error(request, "No tienes permisos para acceder a esta sección.")
      return redirect('homepage')
    return view_func(request, *args, **kwargs)
  return _wrapped_view

@admin_required
@multifactor_protected(factors=1, user_filter={'role': 'ADMIN'}, max_age=60*60*24, advertise=True)
def admin_dashboard(request):
  """Dashboard principal del administrador"""
  # Estadísticas
  stats = {
    'total_users': CustomUser.objects.count(),
    'total_accommodations': Accommodation.objects.count(),
    'total_activities': Activity.objects.count(),
    'total_services': Service.objects.count(),
    'pending_accommodations': Accommodation.objects.filter(status='Pendiente').count(),
    'pending_activities': Activity.objects.filter(status='Pendiente').count(),
    'pending_services': Service.objects.filter(status='Pendiente').count(),
    'recent_approvals': ApprovalLog.objects.order_by('-created_at')[:5]
  }
  
  return render(request, 'admin_panel/dashboard.html', {'stats': stats})

@admin_required
@multifactor_protected(factors=1, user_filter={'role': 'ADMIN'}, max_age=60*60*24, advertise=True)
def pending_approval_list(request):
  """Lista de alojamientos, actividades y servicios pendientes de aprobación"""
  pending_accommodations = Accommodation.objects.filter(status='Pendiente')
  pending_activities = Activity.objects.filter(status='Pendiente')
  pending_services = Service.objects.filter(status='Pendiente')
  
  context = {
    'pending_accommodations': pending_accommodations,
    'pending_activities': pending_activities,
    'pending_services': pending_services
  }

  return render(request, 'admin_panel/pending_approval.html', context)

@admin_required
@multifactor_protected(factors=1, user_filter={'role': 'ADMIN'}, max_age=60*60*24, advertise=True)
def approval_detail(request, item_type, item_id):
  """Detalle de un item para aprobación/rechazo"""
  if item_type == 'accommodation':
    item = get_object_or_404(Accommodation, id=item_id)
    template = 'admin_panel/approval_accommodation_detail.html'
  elif item_type == 'activity':
    item = get_object_or_404(Activity, id=item_id)
    template = 'admin_panel/approval_activity_detail.html'
  elif item_type == 'service':
    item = get_object_or_404(Service, id=item_id)
    template = 'admin_panel/approval_service_detail.html'
  else:
    messages.error(request, "Tipo de ítem inválido.")
    return redirect('admin_panel:admin_pending_approval')

  # Obtener historial de aprobaciones
  approval_logs = ApprovalLog.objects.filter(
    Q(accommodation=item) if item_type == 'accommodation' 
    else Q(activity=item) if item_type == 'activity' 
    else Q(service=item)
  ).order_by('-created_at')

  context = {
    'item': item,
    'item_type': item_type,
    'approval_logs': approval_logs
  }

  return render(request, template, context)

@admin_required
@multifactor_protected(factors=1, user_filter={'role': 'ADMIN'}, max_age=60*60*24, advertise=True)
def approve_item(request, item_type, item_id):
  """Aprobar un item (alojamiento, actividad o servicio)"""
  if request.method == 'POST':
    if item_type == 'accommodation':
      item = get_object_or_404(Accommodation, id=item_id)
    elif item_type == 'activity':
      item = get_object_or_404(Activity, id=item_id)
    elif item_type == 'service':
      item = get_object_or_404(Service, id=item_id)
    else:
      messages.error(request, "Tipo de ítem inválido.")
      return redirect('admin_panel:admin_pending_approval')
    
    # Aprobar el item
    item.status = 'Aprobado'
    item.save()

    # Crear registro en el log
    approval_data = {
      'admin_user': request.user,
      'status': 'approved',
      'notes': request.POST.get('notes', '')
    }

    if item_type == 'accommodation':
      approval_data['accommodation'] = item
    elif item_type == 'activity':
      approval_data['activity'] = item
    else:
      approval_data['service'] = item

    ApprovalLog.objects.create(**approval_data)

    messages.success(request, f"{item_type.capitalize()} '{item.name}' aprobado exitosamente!")
    return redirect('admin_panel:admin_pending_approval')
  
  return redirect('admin_panel:admin_pending_approval')

@admin_required
@multifactor_protected(factors=1, user_filter={'role': 'ADMIN'}, max_age=60*60*24, advertise=True)
def reject_item(request, item_type, item_id):
  """Rechazar un item (alojamiento, actividad o servicio)"""
  if request.method == 'POST':
    if item_type == 'accommodation':
      item = get_object_or_404(Accommodation, id=item_id)
    elif item_type == 'activity':
      item = get_object_or_404(Activity, id=item_id)
    elif item_type == 'service':
      item = get_object_or_404(Service, id=item_id)
    else:
      messages.error(request, "Tipo de ítem inválido.")
      return redirect('admin_panel:admin_pending_approval')
    
    notes = request.POST.get('notes', 'Razón no especificada')

    # Crear registro en el log antes de actualizar el estado
    approval_data = {
      'admin_user': request.user,
      'status': 'rejected',
      'notes': notes
    }

    if item_type == 'accommodation':
      approval_data['accommodation'] = item
    elif item_type == 'activity':
      approval_data['activity'] = item
    else:
      approval_data['service'] = item

    ApprovalLog.objects.create(**approval_data)

    # Actualizar estado a Rechazado en lugar de eliminar
    item.status = 'Rechazado'
    item.save()

    item_name = item.name
    messages.warning(request, f"{item_type.capitalize()} '{item_name}' ha sido rechazado.")
    return redirect('admin_panel:admin_pending_approval')
  
  return redirect('admin_panel:admin_pending_approval')

@admin_required
@multifactor_protected(factors=1, user_filter={'role': 'ADMIN'}, max_age=60*60*24, advertise=True)
def user_list(request):
  """Lista de todos los usuarios registrados"""
  users = CustomUser.objects.all().order_by('-created_at')

  # Estadísticas de usuarios
  user_stats = {
    'total': users.count(),
    'admins': users.filter(role='ADMIN').count(),
    'regular_users': users.filter(role='USER').count(),
    'active_today': users.filter(last_login__date=timezone.now().date()).count() if users.filter(last_login__isnull=False).exists() else 0
  }

  context = {
    'users': users,
    'user_stats': user_stats
  }

  return render(request, 'admin_panel/user_list.html', context)
