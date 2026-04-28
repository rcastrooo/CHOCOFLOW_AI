from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Importación de modelos actualizados
from .models import (
    Usuario, Turno, Asignacion,
    Produccion, Lote, Exportacion, Reporte
)

# ========================
# FUNCIÓN AUXILIAR
# ========================
def parse_body(request):
    """
    Convierte el body de la petición (JSON) a diccionario Python.
    """
    try:
        return json.loads(request.body)
    except:
        return {}


# ========================
# USUARIOS
# ========================
@csrf_exempt
def usuarios(request):
    """
    GET  -> Lista todos los usuarios
    POST -> Crea un usuario (la contraseña se encripta automáticamente en el model)
    """

    # CONSULTAR
    if request.method == "GET":
        data = list(Usuario.objects.values())
        return JsonResponse(data, safe=False)

    # CREAR
    if request.method == "POST":
        body = parse_body(request)

        usuario = Usuario.objects.create(
            nombre=body.get("nombre"),
            email=body.get("email"),
            contrasena=body.get("contrasena"),  # Se encripta en save()
            rol=body.get("rol"),
            estado=body.get("estado", "Activo")
        )

        return JsonResponse({
            "mensaje": "Usuario creado correctamente",
            "id": usuario.id
        })


# ========================
# TURNOS
# ========================
@csrf_exempt
def turnos(request):
    """
    GET  -> Lista turnos
    POST -> Crea turno
    """

    if request.method == "GET":
        data = list(Turno.objects.values())
        return JsonResponse(data, safe=False)

    if request.method == "POST":
        body = parse_body(request)

        turno = Turno.objects.create(
            fecha=body.get("fecha"),
            horario=body.get("horario"),
            hora_inicio=body.get("hora_inicio"),
            hora_fin=body.get("hora_fin")
        )

        return JsonResponse({
            "mensaje": "Turno creado",
            "id": turno.id
        })


# ========================
# ASIGNACIONES
# ========================
@csrf_exempt
def asignaciones(request):
    """
    GET  -> Lista asignaciones
    POST -> Asigna usuario a turno
    """

    if request.method == "GET":
        data = list(Asignacion.objects.values())
        return JsonResponse(data, safe=False)

    if request.method == "POST":
        body = parse_body(request)

        asignacion = Asignacion.objects.create(
            usuario_id=body.get("usuario_id"),
            turno_id=body.get("turno_id"),
            tarea=body.get("tarea"),
            fecha_asignacion=body.get("fecha_asignacion")
        )

        return JsonResponse({
            "mensaje": "Asignación creada",
            "id": asignacion.id
        })


# ========================
# PRODUCCIÓN
# ========================
@csrf_exempt
def producciones(request):
    """
    GET  -> Lista producciones
    POST -> Crea producción
    """

    if request.method == "GET":
        data = list(Produccion.objects.values())
        return JsonResponse(data, safe=False)

    if request.method == "POST":
        body = parse_body(request)

        produccion = Produccion.objects.create(
            producto=body.get("producto"),
            ingredientes=body.get("ingredientes"),
            cantidad_planificada=body.get("cantidad_planificada"),
            fecha_entrega=body.get("fecha_entrega"),
            fecha_limite=body.get("fecha_limite"),
            usuario_id=body.get("usuario_id"),  # opcional
            estado="Pendiente"
        )

        return JsonResponse({
            "mensaje": "Producción creada",
            "id": produccion.id
        })


# ========================
# INICIAR PRODUCCIÓN
# ========================
def iniciar_produccion(request, id):
    """
    Cambia estado de producción a 'En Proceso'
    """
    try:
        produccion = Produccion.objects.get(id=id)
        produccion.estado = "En Proceso"
        produccion.save()

        return JsonResponse({"mensaje": "Producción iniciada"})
    except Produccion.DoesNotExist:
        return JsonResponse({"error": "Producción no encontrada"}, status=404)


# ========================
# FINALIZAR PRODUCCIÓN
# ========================
@csrf_exempt
def finalizar_produccion(request, id):
    """
    Finaliza producción y crea lote automáticamente
    """
    try:
        produccion = Produccion.objects.get(id=id)
        body = parse_body(request)

        cantidad = body.get("cantidad_producida", 0)

        # Actualizar producción
        produccion.estado = "Finalizado"
        produccion.cantidad_producida = cantidad
        produccion.save()

        # Crear lote automáticamente (trazabilidad)
        lote = Lote.objects.create(
            codigo_lote=f"LOTE-{produccion.id}",
            cantidad=cantidad,
            fecha_produccion=produccion.fecha_inicio,
            fecha_vencimiento=produccion.fecha_limite,
            produccion=produccion
        )

        return JsonResponse({
            "mensaje": "Producción finalizada",
            "lote": lote.codigo_lote
        })

    except Produccion.DoesNotExist:
        return JsonResponse({"error": "Producción no encontrada"}, status=404)


# ========================
# LOTES
# ========================
def lotes(request):
    """
    GET -> Lista lotes
    """
    data = list(Lote.objects.values())
    return JsonResponse(data, safe=False)


# ========================
# EXPORTACIONES
# ========================
@csrf_exempt
def exportaciones(request):
    """
    GET  -> Lista exportaciones
    POST -> Crea exportación
    """

    if request.method == "GET":
        data = list(Exportacion.objects.values())
        return JsonResponse(data, safe=False)

    if request.method == "POST":
        body = parse_body(request)

        exportacion = Exportacion.objects.create(
            destino=body.get("destino"),
            pais=body.get("pais"),
            estado="Pendiente"
        )

        return JsonResponse({
            "mensaje": "Exportación creada",
            "id": exportacion.id
        })


# ========================
# ENVIAR EXPORTACIÓN
# ========================
def enviar_exportacion(request, id):
    """
    Cambia estado a 'Enviado'
    """
    try:
        exportacion = Exportacion.objects.get(id=id)
        exportacion.estado = "Enviado"
        exportacion.save()

        return JsonResponse({"mensaje": "Exportación enviada"})
    except Exportacion.DoesNotExist:
        return JsonResponse({"error": "Exportación no encontrada"}, status=404)


# ========================
# CONFIRMAR ENTREGA
# ========================
def confirmar_entrega(request, id):
    """
    Cambia estado a 'Entregado'
    """
    try:
        exportacion = Exportacion.objects.get(id=id)
        exportacion.estado = "Entregado"
        exportacion.save()

        return JsonResponse({"mensaje": "Entrega confirmada"})
    except Exportacion.DoesNotExist:
        return JsonResponse({"error": "Exportación no encontrada"}, status=404)


# ========================
# REPORTES
# ========================
def reportes(request):
    """
    GET -> Lista reportes
    """
    data = list(Reporte.objects.values())
    return JsonResponse(data, safe=False)

# -------------------------------------
# =======================
# LOGICA INDEX
# =======================
from django.shortcuts import render
from .models import Produccion, Exportacion

def index(request):
    # Ejemplo de datos dinámicos (puedes cambiar luego)
    producciones = Produccion.objects.all()[:5]
    exportaciones = Exportacion.objects.all()[:5]

    context = {
        'producciones': producciones,
        'exportaciones': exportaciones
    }

    return render(request, 'index.html', context)