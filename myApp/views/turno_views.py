from django.shortcuts import render, redirect
from myApp.models import Turno

def turnos_lista(request):
    if not request.session.get('usuario_id'):
        return redirect('login')
    turnos = Turno.objects.all()
    return render(request, 'turnos/lista.html', {'turnos': turnos})

def turno_crear(request):
    if not request.session.get('usuario_id'):
        return redirect('login')
    if request.method == 'POST':
        Turno.objects.create(
            fecha=request.POST.get('fecha'),
            horario=request.POST.get('horario'),
            hora_inicio=request.POST.get('hora_inicio'),
            hora_fin=request.POST.get('hora_fin'),
        )
        return redirect('turnos_lista')
    return render(request, 'turnos/crear.html')

def turno_editar(request, id):
    if not request.session.get('usuario_id'):
        return redirect('login')
    turno = Turno.objects.get(id=id)
    if request.method == 'POST':
        turno.fecha = request.POST.get('fecha')
        turno.horario = request.POST.get('horario')
        turno.hora_inicio = request.POST.get('hora_inicio')
        turno.hora_fin = request.POST.get('hora_fin')
        turno.save()
        return redirect('turnos_lista')
    return render(request, 'turnos/editar.html', {'turno': turno})

def turno_eliminar(request, id):
    if not request.session.get('usuario_id'):
        return redirect('login')
    Turno.objects.get(id=id).delete()
    return redirect('turnos_lista')