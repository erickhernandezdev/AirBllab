from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import connection
from django_otp import login as otp_login
from .forms import LoginForm
from .models import YubikeyDevice

def set_user_context(user):
    with connection.cursor() as cursor:
        cursor.execute("SET app.current_user_id = %s;", [user.user_id])

def login_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user, "is_verified") and request.user.is_verified():
            if getattr(request.user, "is_admin", False):
                return redirect('admin_panel:admin_dashboard')
            else:
                return redirect('homepage')
        else:
            return redirect('otp_verify')
    
    if request.method == 'POST':
        form = LoginForm(request.POST, request=request)
        
        if form.is_valid():
            user = form.cleaned_data['user']
            request.session['pre_otp_user_id'] = user.pk

            if YubikeyDevice.objects.filter(user=user, confirmed=True).exists():
                return redirect('otp_verify')
            else:
                login(request, user)
                set_user_context(user)

                if getattr(user, "is_admin", False):
                    return redirect('admin_panel:admin_dashboard')
                else:
                    return redirect('homepage')
        
        return render(request, 'login/login.html', {'form': form})
    
    form = LoginForm()
    return render(request, 'login/login.html', {'form': form})

def otp_verify_view(request):
    user_id = request.session.get('pre_otp_user_id')
    if not user_id:
        return redirect('login')
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.get(pk=user_id)

    devices = YubikeyDevice.objects.filter(user=user, confirmed=True)
    
    if not devices.exists():
        messages.warning(request, 'No tienes Yubikeys configuradas. Por favor contacta al administrador.')
        return redirect('homepage')
    
    if request.method == 'POST':
        otp_token = request.POST.get('otp_token', '').strip()
        
        if not otp_token:
            return render(request, 'login/otp_verify.html', {'devices': devices})

        if len(otp_token) < 32:
            messages.error(request, 'El OTP de Yubikey parece incompleto. Por favor, intenta de nuevo.')
            return render(request, 'login/otp_verify.html', {'devices': devices})
        
        verified = False
        device_used = None
        
        for device in devices:
            if device.verify_token(otp_token):
                verified = True
                device_used = device
                break
        
        if verified:
            from django.contrib.auth import get_backends
            backend = get_backends()[0]
            user.backend = backend.__module__ + "." + backend.__class__.__name__
            login(request, user)
            set_user_context(user)
            otp_login(request, device_used)
            del request.session['pre_otp_user_id']

            if getattr(user, "is_admin", False):
                return redirect('admin_panel:admin_dashboard')
            else:
                return redirect('homepage')
        else:            
            messages.error(request, 'OTP de Yubikey inválido. Por favor, intenta de nuevo.')
    
    return render(request, 'login/otp_verify.html', {'devices': devices})

def logout_view(request):
    """Logout view."""
    logout(request)
    return redirect('homepage')