from django.shortcuts import render
from .forms import NewProposalForm
from .models import Accomodations, Services, Activities

def add_new_proposal(request):
  form = NewProposalForm()
  success = False

  if request.method == 'POST':
    form = NewProposalForm(request.POST)
    if form.is_valid():
      name = form.cleaned_data['name']
      description = form.cleaned_data['description']
      proposal_type = form.cleaned_data['type']
      start_date = form.cleaned_data['start_date']
      end_date = form.cleaned_data['end_date']
      price = form.cleaned_data['price']

      if proposal_type == 'accomodation':
        new_accomodation = Accomodations (
          name=name,
          description=description,
          type=proposal_type,
          start_date=start_date,
          end_date=end_date,
          price=price,
          status='pendiente'
        )
        new_accomodation.save()
      elif proposal_type == 'activity':
        new_activity = Activities (
          name=name,
          description=description,
          type=proposal_type,
          start_date=start_date,
          end_date=end_date,
          price=price,
          status='pendiente'
        )
        new_activity.save()
      else:
        new_service = Services (
          name=name,
          description=description,
          type=proposal_type,
          start_date=start_date,
          end_date=end_date,
          price=price,
          status='pendiente'
        )

        new_service.save()
        
      success = True  
      form = NewProposalForm()

  return render(request, 'new_proposal/new_proposal.html', {'form': form, 'success': success})
