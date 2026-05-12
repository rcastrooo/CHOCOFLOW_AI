from django.contrib import admin
from django.urls import path
from myApp.views import (
    index,
    registro,
    login_usuario,
    logout_view,

    usuarios,
    turnos,
    asignaciones,
    producciones,
    iniciar_produccion,
    finalizar_produccion,
    lotes,
    exportaciones,
    enviar_exportacion,
    confirmar_entrega,
    reportes
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'),

    # AUTH
    path('login/', login_usuario, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registro/', registro, name='registro'),

    # API
    path('usuarios/', usuarios),
    path('turnos/', turnos),
    path('asignaciones/', asignaciones),
    path('producciones/', producciones),
    path('produccion/iniciar/<int:id>/', iniciar_produccion),
    path('produccion/finalizar/<int:id>/', finalizar_produccion),

    path('lotes/', lotes),

    path('exportaciones/', exportaciones),
    path('exportacion/enviar/<int:id>/', enviar_exportacion),
    path('exportacion/entregar/<int:id>/', confirmar_entrega),

    path('reportes/', reportes),
]