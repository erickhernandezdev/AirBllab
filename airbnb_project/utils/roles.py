from django.shortcuts import redirect
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or not getattr(request.user, 'is_admin', False):
            return redirect('homepage')
        return view_func(request, *args, **kwargs)
    return _wrapped

def user_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if getattr(request.user, 'is_admin', False):
            return redirect('admin_panel:admin_dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped
