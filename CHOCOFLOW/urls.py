from django.contrib import admin
from django.urls import path
from myApp.views import (
    index, login_view, logout_view, dashboard, sin_permiso,
    # Usuarios
    usuarios_lista, usuario_crear, usuario_editar, usuario_inactivar,
    # Turnos
    turnos_lista, turno_crear, turno_editar, turno_eliminar,
    # Produccion
    producciones_lista, produccion_crear, produccion_editar,
    produccion_iniciar, produccion_finalizar_form, produccion_eliminar,
    # Exportaciones
    exportaciones_lista, exportacion_crear, exportacion_editar,
    exportacion_enviar, exportacion_entregar, exportacion_eliminar,
    # Asignaciones
    asignaciones_lista, asignacion_crear, asignacion_editar, asignacion_eliminar,
    # Reportes
    reportes_lista,
    # IA
    ia_predicciones,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('sin-permiso/', sin_permiso, name='sin_permiso'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),

    # Usuarios
    path('panel/usuarios/', usuarios_lista, name='usuarios_lista'),
    path('panel/usuarios/crear/', usuario_crear, name='usuario_crear'),
    path('panel/usuarios/editar/<int:id>/', usuario_editar, name='usuario_editar'),
    path('panel/usuarios/inactivar/<int:id>/', usuario_inactivar, name='usuario_inactivar'),

    # Turnos
    path('panel/turnos/', turnos_lista, name='turnos_lista'),
    path('panel/turnos/crear/', turno_crear, name='turno_crear'),
    path('panel/turnos/editar/<int:id>/', turno_editar, name='turno_editar'),
    path('panel/turnos/eliminar/<int:id>/', turno_eliminar, name='turno_eliminar'),

    # Producción
    path('panel/produccion/', producciones_lista, name='producciones_lista'),
    path('panel/produccion/crear/', produccion_crear, name='produccion_crear'),
    path('panel/produccion/editar/<int:id>/', produccion_editar, name='produccion_editar'),
    path('panel/produccion/iniciar/<int:id>/', produccion_iniciar, name='produccion_iniciar'),
    path('panel/produccion/finalizar/<int:id>/', produccion_finalizar_form, name='produccion_finalizar_form'),
    path('panel/produccion/eliminar/<int:id>/', produccion_eliminar, name='produccion_eliminar'),

    # Exportaciones
    path('panel/exportaciones/', exportaciones_lista, name='exportaciones_lista'),
    path('panel/exportaciones/crear/', exportacion_crear, name='exportacion_crear'),
    path('panel/exportaciones/editar/<int:id>/', exportacion_editar, name='exportacion_editar'),
    path('panel/exportaciones/enviar/<int:id>/', exportacion_enviar, name='exportacion_enviar'),
    path('panel/exportaciones/entregar/<int:id>/', exportacion_entregar, name='exportacion_entregar'),
    path('panel/exportaciones/eliminar/<int:id>/', exportacion_eliminar, name='exportacion_eliminar'),

    # Asignaciones
    path('panel/asignaciones/', asignaciones_lista, name='asignaciones_lista'),
    path('panel/asignaciones/crear/', asignacion_crear, name='asignacion_crear'),
    path('panel/asignaciones/editar/<int:id>/', asignacion_editar, name='asignacion_editar'),
    path('panel/asignaciones/eliminar/<int:id>/', asignacion_eliminar, name='asignacion_eliminar'),

    # Reportes
    path('panel/reportes/', reportes_lista, name='reportes_lista'),

    # IA
    path('panel/ia/', ia_predicciones, name='ia_predicciones'),
]
