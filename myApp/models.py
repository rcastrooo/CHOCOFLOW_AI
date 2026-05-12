from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):
    ROL_CHOICES = [('Administrador', 'Administrador'), ('Supervisor', 'Supervisor')]
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
        ('Incapacitado', 'Incapacitado'),
        ('Suspendido', 'Suspendido')
    ]

    nombre = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, max_length=255)
    telefono = models.IntegerField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    contrasena = models.CharField(max_length=255, null=True, blank=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.nombre or ''


class Empleado(models.Model):
    ESTADO_CHOICES = Usuario.ESTADO_CHOICES

    cedula = models.CharField(max_length=20, null=True, blank=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, max_length=255)
    telefono = models.IntegerField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, null=True, blank=True)

    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre or ''


class Turno(models.Model):
    HORARIO_CHOICES = [
        ('Mañana 6:00am - 2:00pm', 'Mañana 6:00am - 2:00pm'),
        ('Tarde 2:00pm - 10:00pm', 'Tarde 2:00pm - 10:00pm')
    ]

    fecha = models.DateField(null=True, blank=True)
    horario = models.CharField(max_length=50, choices=HORARIO_CHOICES, null=True, blank=True)

    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fin = models.TimeField(null=True, blank=True)

    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.fecha} - {self.horario}"


class Asignacion(models.Model):
    tarea = models.CharField(max_length=255, null=True, blank=True)
    fecha_asignacion = models.DateField(null=True, blank=True)

    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    turno = models.ForeignKey(Turno, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.tarea or ''


class Produccion(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Cancelado', 'Cancelado'),
        ('Finalizado', 'Finalizado')
    ]

    producto = models.CharField(max_length=255, null=True, blank=True)
    ingredientes = models.CharField(max_length=255, null=True, blank=True)

    cantidad_planificada = models.CharField(max_length=255, null=True, blank=True)
    cantidad_producida = models.CharField(max_length=255, null=True, blank=True)

    fecha_entrega = models.DateField(null=True, blank=True)
    fecha_limite = models.DateField(null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="Pendiente")

    empleado_responsable = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.producto} - {self.estado}"


class Exportacion(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Enviado', 'Enviado'),
        ('Entregado', 'Entregado'),
        ('Cancelado', 'Cancelado')
    ]

    destino = models.CharField(max_length=255, null=True, blank=True)
    pais = models.CharField(max_length=255, null=True, blank=True)

    fecha_envio = models.DateField(null=True, blank=True)
    fecha_entrega = models.DateField(null=True, blank=True)

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="Pendiente")

    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.destino or ''


class Lote(models.Model):
    codigo_lote = models.CharField(max_length=100, unique=True)
    cantidad = models.IntegerField(null=True, blank=True)

    fecha_produccion = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)

    produccion = models.ForeignKey(Produccion, on_delete=models.SET_NULL, null=True, blank=True)
    exportacion = models.ForeignKey(Exportacion, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.codigo_lote


# ✅ ESTE ES EL QUE TE FALTABA
class Reporte(models.Model):
    titulo = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titulo or ''