from django.shortcuts import render, redirect
from .forms import LoginForm

def login(request):
    if request.method == 'POST':
      form = LoginForm(request.POST)
      if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        return redirect('home')

    form = LoginForm()
    return render(request, 'login/login.html', {'form': form})

