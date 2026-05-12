from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import json

from .models import (
    Usuario, Turno, Asignacion,
    Produccion, Lote, Exportacion, Reporte
)

# =====================
# AUTH
# =====================

def index(request):
    return render(request, "index.html")


def registro(request):
    if request.method == 'POST':
        identificacion = request.POST['identificacion']
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        password = request.POST['password']

        if User.objects.filter(username=identificacion).exists():
            messages.error(request, "Usuario ya existe")
            return redirect('registro')

        User.objects.create_user(
            username=identificacion,
            first_name=nombre,
            email=correo,
            password=password
        )

        return redirect('login')

    return render(request, "auth/registro.html")


def login_usuario(request):
    if request.method == 'POST':
        correo = request.POST['username']
        password = request.POST['password']

        try:
            user_obj = User.objects.get(email=correo)
            user = authenticate(request, username=user_obj.username, password=password)
        except:
            user = None

        if user:
            login(request, user)
            return redirect('index')

        messages.error(request, "Error login")

    return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    return redirect('login')


# =====================
# HELPERS
# =====================

def parse_body(request):
    try:
        return json.loads(request.body)
    except:
        return {}


# =====================
# CRUDS
# =====================

@csrf_exempt
def usuarios(request):
    if request.method == "GET":
        return JsonResponse(list(Usuario.objects.values()), safe=False)

    body = parse_body(request)
    u = Usuario.objects.create(**body)
    return JsonResponse({"id": u.id})


@csrf_exempt
def turnos(request):
    if request.method == "GET":
        return JsonResponse(list(Turno.objects.values()), safe=False)

    body = parse_body(request)
    t = Turno.objects.create(**body)
    return JsonResponse({"id": t.id})


@csrf_exempt
def asignaciones(request):
    if request.method == "GET":
        return JsonResponse(list(Asignacion.objects.values()), safe=False)

    body = parse_body(request)
    a = Asignacion.objects.create(**body)
    return JsonResponse({"id": a.id})


@csrf_exempt
def producciones(request):
    if request.method == "GET":
        return JsonResponse(list(Produccion.objects.values()), safe=False)

    body = parse_body(request)
    p = Produccion.objects.create(**body)
    return JsonResponse({"id": p.id})


def iniciar_produccion(request, id):
    p = Produccion.objects.get(id=id)
    p.estado = "En Proceso"
    p.save()
    return JsonResponse({"ok": True})


@csrf_exempt
def finalizar_produccion(request, id):
    p = Produccion.objects.get(id=id)
    body = parse_body(request)

    p.estado = "Finalizado"
    p.cantidad_producida = body.get("cantidad_producida")
    p.save()

    lote = Lote.objects.create(
        codigo_lote=f"LOTE-{p.id}",
        cantidad=p.cantidad_producida,
        produccion=p
    )

    return JsonResponse({"lote": lote.codigo_lote})


def lotes(request):
    return JsonResponse(list(Lote.objects.values()), safe=False)


@csrf_exempt
def exportaciones(request):
    if request.method == "GET":
        return JsonResponse(list(Exportacion.objects.values()), safe=False)

    body = parse_body(request)
    e = Exportacion.objects.create(**body)
    return JsonResponse({"id": e.id})


def enviar_exportacion(request, id):
    e = Exportacion.objects.get(id=id)
    e.estado = "Enviado"
    e.save()
    return JsonResponse({"ok": True})


def confirmar_entrega(request, id):
    e = Exportacion.objects.get(id=id)
    e.estado = "Entregado"
    e.save()
    return JsonResponse({"ok": True})


def reportes(request):
    return JsonResponse(list(Reporte.objects.values()), safe=False)