from django.shortcuts import render, redirect
from myApp.models import Usuario
from myApp.decorators import solo_administrador


@solo_administrador
def usuarios_lista(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})


@solo_administrador
def usuario_crear(request):
    if request.method == 'POST':
        Usuario.objects.create(
            nombre=request.POST.get('nombre'),
            email=request.POST.get('email'),
            contrasena=request.POST.get('contrasena'),
            rol=request.POST.get('rol'),
            estado=request.POST.get('estado'),
        )
        return redirect('usuarios_lista')
    return render(request, 'usuarios/crear.html')


@solo_administrador
def usuario_editar(request, id):
    usuario = Usuario.objects.get(id=id)
    if request.method == 'POST':
        usuario.nombre = request.POST.get('nombre')
        usuario.email = request.POST.get('email')
        usuario.rol = request.POST.get('rol')
        usuario.estado = request.POST.get('estado')
        usuario.save()
        return redirect('usuarios_lista')
    return render(request, 'usuarios/editar.html', {'usuario': usuario})


@solo_administrador
def usuario_inactivar(request, id):
    usuario = Usuario.objects.get(id=id)
    usuario.estado = 'Inactivo'
    usuario.save()
    return redirect('usuarios_lista')