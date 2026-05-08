from django.shortcuts import render, redirect
from django.utils import timezone
from myApp.models import Exportacion
from myApp.decorators import administrador_o_supervisor, solo_administrador


@administrador_o_supervisor
def exportaciones_lista(request):
    exportaciones = Exportacion.objects.all().order_by('-id')
    return render(request, 'exportaciones/lista.html', {'exportaciones': exportaciones})


@administrador_o_supervisor
def exportacion_crear(request):
    if request.method == 'POST':
        Exportacion.objects.create(
            destino=request.POST.get('destino'),
            pais=request.POST.get('pais'),
            fecha_envio=request.POST.get('fecha_envio') or None,
            fecha_entrega=request.POST.get('fecha_entrega') or None,
            estado='Pendiente',
        )
        return redirect('exportaciones_lista')
    return render(request, 'exportaciones/crear.html')


@administrador_o_supervisor
def exportacion_editar(request, id):
    exportacion = Exportacion.objects.get(id=id)
    if request.method == 'POST':
        exportacion.destino = request.POST.get('destino')
        exportacion.pais = request.POST.get('pais')
        exportacion.fecha_envio = request.POST.get('fecha_envio') or None
        exportacion.fecha_entrega = request.POST.get('fecha_entrega') or None
        exportacion.estado = request.POST.get('estado')
        exportacion.save()
        return redirect('exportaciones_lista')
    return render(request, 'exportaciones/editar.html', {'exportacion': exportacion})


@administrador_o_supervisor
def exportacion_enviar(request, id):
    exportacion = Exportacion.objects.get(id=id)
    exportacion.estado = 'Enviado'
    exportacion.fecha_envio = timezone.now().date()
    exportacion.save()
    return redirect('exportaciones_lista')


@administrador_o_supervisor
def exportacion_entregar(request, id):
    exportacion = Exportacion.objects.get(id=id)
    exportacion.estado = 'Entregado'
    exportacion.fecha_entrega = timezone.now().date()
    exportacion.save()
    return redirect('exportaciones_lista')


@solo_administrador
def exportacion_eliminar(request, id):
    Exportacion.objects.get(id=id).delete()
    return redirect('exportaciones_lista')