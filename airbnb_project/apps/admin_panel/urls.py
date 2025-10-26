from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
  path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
  path('pending-approval/', views.pending_approval_list, name='admin_pending_approval'),
  path('approval/<str:item_type>/<int:item_id>/', views.approval_detail, name='admin_approval_detail'),
  path('approve/<str:item_type>/<int:item_id>/', views.approve_item, name='admin_approve_item'),
  path('reject/<str:item_type>/<int:item_id>/', views.reject_item, name='admin_reject_item'),
  
  # Rutas para propuestas
  path('proposal/<str:item_type>/<int:item_id>/', views.proposal_detail, name='admin_proposal_detail'),
  path('proposal/approve/<str:item_type>/<int:item_id>/', views.approve_proposal, name='admin_approve_proposal'),
  path('proposal/reject/<str:item_type>/<int:item_id>/', views.reject_proposal, name='admin_reject_proposal'),
  
  path('users/', views.user_list, name='admin_user_list'),
]
