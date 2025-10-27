from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import login, logout

def login_view(request):
    if request.method == 'POST':
      form = LoginForm(request.POST, request=request)
      if form.is_valid():
        user = form.cleaned_data['user']
        login(request, user)
        return redirect('homepage')
      
      return render(request, 'login/login.html', {'form': form})

    form = LoginForm()
    return render(request, 'login/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('homepage')

