from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

def registro(request):

    if request.method == 'POST':

        identificacion = request.POST['identificacion'].strip()
        nombre = request.POST['nombre'].strip()
        correo = request.POST['correo'].strip()
        password = request.POST['password'].strip()
        rol = request.POST['rol']
        estado = request.POST['estado']

        # ========================
        # VALIDACIONES DE CAMPOS
        # ========================

        # Identificación: solo números, mínimo 5 dígitos
        if not identificacion.isdigit():
            messages.error(request, "La identificación solo debe contener números.")
            return redirect('registro')

        if len(identificacion) < 5:
            messages.error(request, "La identificación debe tener al menos 5 dígitos.")
            return redirect('registro')

        # Nombre: solo letras y espacios, mínimo 3 caracteres
        if not all(c.isalpha() or c.isspace() for c in nombre):
            messages.error(request, "El nombre solo debe contener letras.")
            return redirect('registro')

        if len(nombre) < 3:
            messages.error(request, "El nombre debe tener al menos 3 caracteres.")
            return redirect('registro')

        # Correo: formato válido
        import re
        patron_correo = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        if not re.match(patron_correo, correo):
            messages.error(request, "El correo no tiene un formato válido.")
            return redirect('registro')

        # Contraseña: mínimo 8 caracteres, una mayúscula y un número
        if len(password) < 8:
            messages.error(request, "La contraseña debe tener al menos 8 caracteres.")
            return redirect('registro')

        if not any(c.isupper() for c in password):
            messages.error(request, "La contraseña debe tener al menos una mayúscula.")
            return redirect('registro')

        if not any(c.isdigit() for c in password):
            messages.error(request, "La contraseña debe tener al menos un número.")
            return redirect('registro')

        # Rol y estado: no pueden estar vacíos
        if not rol:
            messages.error(request, "Debes seleccionar un rol.")
            return redirect('registro')

        if not estado:
            messages.error(request, "Debes seleccionar un estado.")
            return redirect('registro')

        # ========================
        # VALIDACIONES DE BD
        # ========================

        if User.objects.filter(username=identificacion).exists():
            messages.error(request, "Esa identificación ya está registrada.")
            return redirect('registro')

        if User.objects.filter(email=correo).exists():
            messages.error(request, "Ese correo ya está registrado.")
            return redirect('registro')

        # ========================
        # CREAR USUARIO
        # ========================
        User.objects.create_user(
            username=identificacion,
            first_name=nombre,
            email=correo,
            password=password
        )

        messages.success(request, "Usuario registrado correctamente ")
        return redirect('login')

    return render(request, 'auth/registro.html')


def login_usuario(request):
    if request.method == 'POST':
        correo = request.POST['username'].strip()
        password = request.POST['password'].strip()

        # ========================
        # VALIDACIONES
        # ========================

        # Campos vacíos
        if not correo or not password:
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, 'auth/login.html')

        # Formato correo
        import re
        patron_correo = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        if not re.match(patron_correo, correo):
            messages.error(request, "El correo no tiene un formato válido.")
            return render(request, 'auth/login.html')

        # ========================
        # AUTENTICACIÓN
        # ========================
        from django.contrib.auth.models import User
        try:
            user_obj = User.objects.get(email=correo)
            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )
        except User.DoesNotExist:
            user = None

        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Correo o contraseña incorrectos ")

    return render(request, 'auth/login.html')

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