from functools import wraps
from django.shortcuts import redirect


def login_requerido(func):
    """Verifica que el usuario tenga sesión activa."""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            return redirect('login')
        return func(request, *args, **kwargs)
    return wrapper


def solo_administrador(func):
    """Solo permite acceso al rol Administrador."""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            return redirect('login')
        if request.session.get('usuario_rol') != 'Administrador':
            return redirect('sin_permiso')
        return func(request, *args, **kwargs)
    return wrapper


def solo_supervisor(func):
    """Solo permite acceso al rol Supervisor."""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            return redirect('login')
        if request.session.get('usuario_rol') != 'Supervisor':
            return redirect('sin_permiso')
        return func(request, *args, **kwargs)
    return wrapper


def administrador_o_supervisor(func):
    """Permite acceso a Administrador y Supervisor."""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            return redirect('login')
        rol = request.session.get('usuario_rol')
        if rol not in ('Administrador', 'Supervisor'):
            return redirect('sin_permiso')
        return func(request, *args, **kwargs)
    return wrapper