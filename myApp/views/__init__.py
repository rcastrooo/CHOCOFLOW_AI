from django.shortcuts import render, redirect
from myApp.models import Produccion, Exportacion, Usuario


def index(request):
    producciones = Produccion.objects.all()[:3]
    exportaciones = Exportacion.objects.all()[:3]
    context = {
        'producciones': producciones,
        'exportaciones': exportaciones,
        'total_producciones': Produccion.objects.count(),
        'total_exportaciones': Exportacion.objects.count(),
        'total_usuarios': Usuario.objects.count(),
    }
    return render(request, 'index.html', context)


def dashboard(request):
    if not request.session.get('usuario_id'):
        return redirect('login')
    context = {
        'usuario_nombre': request.session.get('usuario_nombre'),
        'usuario_rol': request.session.get('usuario_rol'),
        'total_usuarios': Usuario.objects.count(),
        'total_producciones': Produccion.objects.count(),
        'total_exportaciones': Exportacion.objects.count(),
        'producciones_pendientes': Produccion.objects.filter(estado='Pendiente').count(),
        'producciones_en_proceso': Produccion.objects.filter(estado='En Proceso').count(),
        'producciones_finalizadas': Produccion.objects.filter(estado='Finalizado').count(),
        'exportaciones_pendientes': Exportacion.objects.filter(estado='Pendiente').count(),
        'exportaciones_enviadas': Exportacion.objects.filter(estado='Enviado').count(),
        'exportaciones_entregadas': Exportacion.objects.filter(estado='Entregado').count(),
    }
    return render(request, 'dashboard.html', context)


from myApp.views.auth_views import login_view, logout_view
from myApp.views.usuario_views import usuarios_lista, usuario_crear, usuario_editar, usuario_inactivar
from myApp.views.turno_views import turnos_lista, turno_crear, turno_editar, turno_eliminar
from myApp.views.produccion_views import (
    producciones_lista, produccion_crear, produccion_editar,
    produccion_iniciar, produccion_finalizar_form, produccion_eliminar
)
from myApp.views.exportacion_views import (
    exportaciones_lista, exportacion_crear, exportacion_editar,
    exportacion_enviar, exportacion_entregar, exportacion_eliminar
)
from myApp.views.asignacion_views import (
    asignaciones_lista, asignacion_crear, asignacion_editar, asignacion_eliminar
)
from myApp.views.reporte_views import reportes_lista
from myApp.views.ia_views import ia_predicciones
