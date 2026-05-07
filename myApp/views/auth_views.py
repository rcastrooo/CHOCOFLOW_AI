from django.shortcuts import render, redirect
from django.contrib import messages
from myApp.models import Usuario

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        contrasena = request.POST.get('contrasena')

        try:
            usuario = Usuario.objects.get(email=email, contrasena=contrasena)
            request.session['usuario_id'] = usuario.id
            request.session['usuario_nombre'] = usuario.nombre
            request.session['usuario_rol'] = usuario.rol
            return redirect('dashboard')
        except Usuario.DoesNotExist:
            messages.error(request, 'Correo o contraseña incorrectos')

    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')