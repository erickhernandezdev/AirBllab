from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.db import connection

from .forms import LoginForm


def set_user_context(user):
    with connection.cursor() as cursor:
        cursor.execute("SET app.current_user_id = %s;", [user.user_id])


def login_view(request):
    if request.user.is_authenticated:
        if getattr(request.user, "is_admin", False):
            return redirect('admin_panel:admin_dashboard')
        return redirect('homepage')

    if request.method == 'POST':
        form = LoginForm(request.POST, request=request)

        if form.is_valid():
            user = form.cleaned_data['user']

            login(request, user)
            set_user_context(user)

            if getattr(user, "is_admin", False):
                return redirect('admin_panel:admin_dashboard')

            next_url = request.POST.get('next') or request.GET.get('next')

            if next_url:
                return redirect(next_url)

            return redirect('homepage')

        return render(request, 'login/login.html', {'form': form})

    form = LoginForm()
    return render(request, 'login/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('homepage')
