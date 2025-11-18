from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import login, logout
from django.db import connection

def set_user_context(user):
    with connection.cursor() as cursor:
        cursor.execute("SET app.current_user_id = %s;", [user.user_id])

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, request=request)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            set_user_context(user)

            if user.is_admin:
                return redirect('admin_panel:admin_dashboard')
            return redirect('homepage')

        return render(request, 'login/login.html', {'form': form})

    form = LoginForm()
    return render(request, 'login/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('homepage')

