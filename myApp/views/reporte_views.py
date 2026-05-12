from django.shortcuts import render, redirect
from django.db.models import Count
from myApp.models import Usuario, Turno, Asignacion, Produccion, Lote, Exportacion


def reportes_lista(request):
    if not request.session.get('usuario_id'):
        return redirect('login')

    context = {
        'total_usuarios': Usuario.objects.count(),
        'total_turnos': Turno.objects.count(),
        'total_asignaciones': Asignacion.objects.count(),
        'total_producciones': Produccion.objects.count(),
        'total_lotes': Lote.objects.count(),
        'total_exportaciones': Exportacion.objects.count(),

        # Producción por estado
        'prod_pendientes': Produccion.objects.filter(estado='Pendiente').count(),
        'prod_en_proceso': Produccion.objects.filter(estado='En Proceso').count(),
        'prod_finalizadas': Produccion.objects.filter(estado='Finalizado').count(),

        # Exportaciones por estado
        'exp_pendientes': Exportacion.objects.filter(estado='Pendiente').count(),
        'exp_enviadas': Exportacion.objects.filter(estado='Enviado').count(),
        'exp_entregadas': Exportacion.objects.filter(estado='Entregado').count(),

        # Usuarios por rol
        'usuarios_por_rol': Usuario.objects.values('rol').annotate(total=Count('id')).order_by('-total'),

        # Últimas producciones
        'ultimas_producciones': Produccion.objects.all().order_by('-id')[:5],
    }
    return render(request, 'reportes/lista.html', context)
