from django.shortcuts import render, redirect
from myApp.models import Asignacion, Usuario, Turno
from myApp.decorators import administrador_o_supervisor, solo_administrador


@administrador_o_supervisor
def asignaciones_lista(request):
    asignaciones = Asignacion.objects.select_related('usuario', 'turno').all().order_by('-id')
    return render(request, 'asignaciones/lista.html', {'asignaciones': asignaciones})


@administrador_o_supervisor
def asignacion_crear(request):
    if request.method == 'POST':
        Asignacion.objects.create(
            usuario_id=request.POST.get('usuario_id'),
            turno_id=request.POST.get('turno_id'),
            tarea=request.POST.get('tarea'),
            fecha_asignacion=request.POST.get('fecha_asignacion'),
        )
        return redirect('asignaciones_lista')
    usuarios = Usuario.objects.filter(estado='Activo')
    turnos = Turno.objects.all().order_by('-fecha')
    return render(request, 'asignaciones/crear.html', {'usuarios': usuarios, 'turnos': turnos})


@administrador_o_supervisor
def asignacion_editar(request, id):
    asignacion = Asignacion.objects.get(id=id)
    if request.method == 'POST':
        asignacion.usuario_id = request.POST.get('usuario_id')
        asignacion.turno_id = request.POST.get('turno_id')
        asignacion.tarea = request.POST.get('tarea')
        asignacion.fecha_asignacion = request.POST.get('fecha_asignacion')
        asignacion.save()
        return redirect('asignaciones_lista')
    usuarios = Usuario.objects.filter(estado='Activo')
    turnos = Turno.objects.all().order_by('-fecha')
    return render(request, 'asignaciones/editar.html', {
        'asignacion': asignacion,
        'usuarios': usuarios,
        'turnos': turnos,
    })


@solo_administrador
def asignacion_eliminar(request, id):
    Asignacion.objects.get(id=id).delete()
    return redirect('asignaciones_lista')