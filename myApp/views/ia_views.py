from django.shortcuts import render, redirect
from django.utils import timezone
from myApp.models import Produccion, Exportacion, Asignacion, Turno, Usuario
from datetime import date, timedelta
from myApp.decorators import solo_administrador


@solo_administrador
def ia_predicciones(request):
    prediccion = None

    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        hoy = date.today()

        if tipo == 'produccion':
            producciones = Produccion.objects.all()
            total = producciones.count()
            finalizadas = producciones.filter(estado='Finalizado')
            en_proceso = producciones.filter(estado='En Proceso').count()
            pendientes = producciones.filter(estado='Pendiente').count()

            eficiencia_items = []
            for p in finalizadas:
                if p.cantidad_planificada and p.cantidad_planificada > 0:
                    eficiencia_items.append((p.cantidad_producida / p.cantidad_planificada) * 100)
            eficiencia = round(sum(eficiencia_items) / len(eficiencia_items), 1) if eficiencia_items else 0

            productos = {}
            for p in finalizadas:
                productos[p.producto] = productos.get(p.producto, 0) + p.cantidad_producida
            top_productos = sorted(productos.items(), key=lambda x: x[1], reverse=True)[:3]

            retrasadas = producciones.filter(
                estado__in=['Pendiente', 'En Proceso'],
                fecha_limite__lt=timezone.now()
            ).count()

            promedio_semanal = round(total / 4) if total > 0 else 0

            lineas = []
            lineas.append("📦 PREDICCIÓN DE PRODUCCIÓN")
            lineas.append("=" * 40)
            lineas.append(f"\n📊 Estado actual del sistema:")
            lineas.append(f"  • Total producciones: {total}")
            lineas.append(f"  • En proceso: {en_proceso}")
            lineas.append(f"  • Pendientes: {pendientes}")
            lineas.append(f"  • Finalizadas: {finalizadas.count()}")
            lineas.append(f"\n🎯 Eficiencia promedio: {eficiencia}%")

            if eficiencia >= 90:
                lineas.append("  ✅ Excelente rendimiento de producción")
            elif eficiencia >= 70:
                lineas.append("  ⚠️ Rendimiento aceptable, hay margen de mejora")
            else:
                lineas.append("  ❌ Rendimiento bajo, revisar procesos")

            lineas.append(f"\n🔮 Predicción próxima semana:")
            lineas.append(f"  • Se estima {promedio_semanal} órdenes de producción")
            if top_productos:
                lineas.append(f"  • Productos con mayor demanda:")
                for prod, cant in top_productos:
                    lineas.append(f"    - {prod}: {cant} unidades producidas históricamente")

            if retrasadas > 0:
                lineas.append(f"\n🚨 ALERTAS:")
                lineas.append(f"  • {retrasadas} producción(es) con fecha límite vencida")
                lineas.append(f"  • Acción recomendada: revisar y reasignar recursos")
            else:
                lineas.append(f"\n✅ Sin alertas de retraso actualmente")

            lineas.append(f"\n💡 Recomendaciones:")
            if pendientes > en_proceso:
                lineas.append(f"  • Hay {pendientes} pendientes vs {en_proceso} en proceso")
                lineas.append(f"  • Considera iniciar más órdenes para balancear la carga")
            if eficiencia < 80 and total > 0:
                lineas.append(f"  • La eficiencia es menor al 80%, revisar tiempos de producción")
            lineas.append(f"  • Mantener al menos {max(2, en_proceso)} líneas activas simultáneamente")

            prediccion = {'tipo': tipo, 'texto': '\n'.join(lineas)}

        elif tipo == 'exportaciones':
            exportaciones = Exportacion.objects.all()
            total = exportaciones.count()
            pendientes = exportaciones.filter(estado='Pendiente')
            enviadas = exportaciones.filter(estado='Enviado')
            entregadas = exportaciones.filter(estado='Entregado').count()

            en_riesgo = []
            for e in list(pendientes) + list(enviadas):
                if e.fecha_entrega and e.fecha_entrega <= hoy + timedelta(days=7):
                    en_riesgo.append(e)

            paises = {}
            for e in exportaciones:
                paises[e.pais] = paises.get(e.pais, 0) + 1
            top_paises = sorted(paises.items(), key=lambda x: x[1], reverse=True)[:3]

            tasa = round((entregadas / total) * 100, 1) if total > 0 else 0

            lineas = []
            lineas.append("🚚 PREDICCIÓN DE EXPORTACIONES")
            lineas.append("=" * 40)
            lineas.append(f"\n📊 Estado actual:")
            lineas.append(f"  • Total exportaciones: {total}")
            lineas.append(f"  • Pendientes: {pendientes.count()}")
            lineas.append(f"  • Enviadas: {enviadas.count()}")
            lineas.append(f"  • Entregadas: {entregadas}")
            lineas.append(f"\n📈 Tasa de entrega exitosa: {tasa}%")

            if tasa >= 80:
                lineas.append("  ✅ Buen historial de entregas")
            elif tasa >= 50:
                lineas.append("  ⚠️ Tasa de entrega mejorable")
            elif total > 0:
                lineas.append("  ❌ Tasa de entrega baja, revisar logística")

            if top_paises:
                lineas.append(f"\n🌍 Destinos más frecuentes:")
                for pais, cant in top_paises:
                    lineas.append(f"  • {pais}: {cant} exportación(es)")

            if en_riesgo:
                lineas.append(f"\n🚨 ALERTAS — Exportaciones próximas a vencer:")
                for e in en_riesgo:
                    dias = (e.fecha_entrega - hoy).days if e.fecha_entrega else 0
                    lineas.append(f"  • {e.destino} ({e.pais}) — {dias} día(s) restantes — Estado: {e.estado}")
            else:
                lineas.append(f"\n✅ No hay exportaciones en riesgo inmediato")

            lineas.append(f"\n🔮 Predicción:")
            if pendientes.count() > 0:
                lineas.append(f"  • {pendientes.count()} exportación(es) pendientes de envío")
                lineas.append(f"  • Se recomienda procesar en los próximos 3 días")
            if enviadas.count() > 0:
                lineas.append(f"  • {enviadas.count()} exportación(es) en tránsito")

            lineas.append(f"\n💡 Recomendaciones:")
            lineas.append(f"  • Confirmar fechas de entrega con transportistas")
            lineas.append(f"  • Actualizar estados regularmente en el sistema")
            if tasa < 80 and total > 0:
                lineas.append(f"  • Analizar causas de retrasos en entregas anteriores")

            prediccion = {'tipo': tipo, 'texto': '\n'.join(lineas)}

        elif tipo == 'asignaciones':
            asignaciones = Asignacion.objects.select_related('usuario', 'turno').all()
            total = asignaciones.count()
            empleados_activos = Usuario.objects.filter(estado='Activo').count()

            carga = {}
            for a in asignaciones:
                nombre = a.usuario.nombre
                carga[nombre] = carga.get(nombre, 0) + 1
            sobrecargados = [(n, c) for n, c in carga.items() if c >= 3]

            manana = asignaciones.filter(turno__horario='Mañana').count()
            tarde = asignaciones.filter(turno__horario='Tarde').count()
            promedio = round(total / empleados_activos, 1) if empleados_activos > 0 else 0

            lineas = []
            lineas.append("👥 PREDICCIÓN DE ASIGNACIONES")
            lineas.append("=" * 40)
            lineas.append(f"\n📊 Estado actual:")
            lineas.append(f"  • Empleados activos: {empleados_activos}")
            lineas.append(f"  • Total asignaciones: {total}")
            lineas.append(f"  • Promedio por empleado: {promedio} tareas")
            lineas.append(f"\n⏰ Distribución por turno:")
            lineas.append(f"  • Turno Mañana: {manana} asignaciones")
            lineas.append(f"  • Turno Tarde: {tarde} asignaciones")

            if manana > tarde * 1.5:
                lineas.append(f"  ⚠️ Turno mañana sobrecargado vs tarde")
            elif tarde > manana * 1.5:
                lineas.append(f"  ⚠️ Turno tarde sobrecargado vs mañana")
            else:
                lineas.append(f"  ✅ Distribución de turnos equilibrada")

            if sobrecargados:
                lineas.append(f"\n🚨 Empleados con alta carga de trabajo:")
                for nombre, cant in sobrecargados:
                    lineas.append(f"  • {nombre}: {cant} tareas asignadas")
            else:
                lineas.append(f"\n✅ Ningún empleado con sobrecarga detectada")

            lineas.append(f"\n🔮 Predicción próxima semana:")
            recomendado = max(2, round(empleados_activos * 0.5))
            lineas.append(f"  • Turno Mañana: se recomiendan {recomendado} empleados")
            lineas.append(f"  • Turno Tarde: se recomiendan {recomendado} empleados")

            lineas.append(f"\n💡 Recomendaciones:")
            if empleados_activos < 3:
                lineas.append(f"  • Considera activar más empleados, solo hay {empleados_activos} activos")
            if promedio > 4:
                lineas.append(f"  • Promedio de {promedio} tareas/empleado es alto, redistribuir carga")
            lineas.append(f"  • Rotar empleados entre turnos para evitar fatiga")
            lineas.append(f"  • Asignar tareas según el rol de cada empleado")

            prediccion = {'tipo': tipo, 'texto': '\n'.join(lineas)}

    context = {
        'prediccion': prediccion,
        'total_producciones': Produccion.objects.count(),
        'total_exportaciones': Exportacion.objects.count(),
        'total_asignaciones': Asignacion.objects.count(),
    }
    return render(request, 'ia/predicciones.html', context)