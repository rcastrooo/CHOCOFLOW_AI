from django.shortcuts import render, redirect
from django.utils import timezone
from myApp.models import Exportacion


def exportaciones_lista(request):
    if not request.session.get('usuario_id'):
        return redirect('login')
    exportaciones = Exportacion.objects.all().order_by('-id')
    return render(request, 'exportaciones/lista.html', {'exportaciones': exportaciones})


def exportacion_crear(request):
    if not request.session.get('usuario_id'):
        return redirect('login')
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


def exportacion_editar(request, id):
    if not request.session.get('usuario_id'):
        return redirect('login')
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


def exportacion_enviar(request, id):
    if not request.session.get('usuario_id'):
        return redirect('login')
    exportacion = Exportacion.objects.get(id=id)
    exportacion.estado = 'Enviado'
    exportacion.fecha_envio = timezone.now().date()
    exportacion.save()
    return redirect('exportaciones_lista')


def exportacion_entregar(request, id):
    if not request.session.get('usuario_id'):
        return redirect('login')
    exportacion = Exportacion.objects.get(id=id)
    exportacion.estado = 'Entregado'
    exportacion.fecha_entrega = timezone.now().date()
    exportacion.save()
    return redirect('exportaciones_lista')


def exportacion_eliminar(request, id):
    if not request.session.get('usuario_id'):
        return redirect('login')
    Exportacion.objects.get(id=id).delete()
    return redirect('exportaciones_lista')
