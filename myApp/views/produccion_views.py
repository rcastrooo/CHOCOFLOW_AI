from django.shortcuts import render, redirect
from django.utils import timezone
from myApp.models import Produccion, Lote, Usuario


def producciones_lista(request):
    if not request.session.get('usuario_id'):
        return redirect('login')
    producciones = Produccion.objects.all().order_by('-id')
    return render(request, 'produccion/lista.html', {'producciones': producciones})


def produccion_crear(request):
    if not request.session.get('usuario_id'):
        return redirect('login')
    if request.method == 'POST':
        usuario = Usuario.objects.get(id=request.session.get('usuario_id'))
        Produccion.objects.create(
            producto=request.POST.get('producto'),
            ingredientes=request.POST.get('ingredientes'),
            cantidad_planificada=request.POST.get('cantidad_planificada'),
            cantidad_producida=0,
            fecha_entrega=request.POST.get('fecha_entrega'),
            fecha_limite=request.POST.get('fecha_limite'),
            estado='Pendiente',
            usuario=usuario,
        )
        return redirect('producciones_lista')
    return render(request, 'produccion/crear.html')


def produccion_editar(request, id):
    if not request.session.get('usuario_id'):
        return redirect('login')
    produccion = Produccion.objects.get(id=id)
    if request.method == 'POST':
        produccion.producto = request.POST.get('producto')
        produccion.ingredientes = request.POST.get('ingredientes')
        produccion.cantidad_planificada = request.POST.get('cantidad_planificada')
        produccion.fecha_entrega = request.POST.get('fecha_entrega')
        produccion.fecha_limite = request.POST.get('fecha_limite')
        produccion.save()
        return redirect('producciones_lista')
    return render(request, 'produccion/editar.html', {'produccion': produccion})


def produccion_iniciar(request, id):
    if not request.session.get('usuario_id'):
        return redirect('login')
    produccion = Produccion.objects.get(id=id)
    produccion.estado = 'En Proceso'
    produccion.fecha_inicio = timezone.now()
    produccion.save()
    return redirect('producciones_lista')


def produccion_finalizar_form(request, id):
    if not request.session.get('usuario_id'):
        return redirect('login')
    produccion = Produccion.objects.get(id=id)
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad_producida', produccion.cantidad_planificada))
        produccion.estado = 'Finalizado'
        produccion.fecha_fin = timezone.now()
        produccion.cantidad_producida = cantidad
        produccion.save()
        Lote.objects.create(
            codigo_lote=f"LOTE-{produccion.id}-{timezone.now().strftime('%Y%m%d')}",
            cantidad=cantidad,
            fecha_produccion=produccion.fecha_inicio.date() if produccion.fecha_inicio else timezone.now().date(),
            fecha_vencimiento=produccion.fecha_limite.date() if produccion.fecha_limite else timezone.now().date(),
            produccion=produccion,
        )
        return redirect('producciones_lista')
    return render(request, 'produccion/finalizar.html', {'produccion': produccion})


def produccion_eliminar(request, id):
    if not request.session.get('usuario_id'):
        return redirect('login')
    Produccion.objects.get(id=id).delete()
    return redirect('producciones_lista')
