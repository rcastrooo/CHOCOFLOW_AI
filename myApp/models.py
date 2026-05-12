from django.db import models
from django.contrib.auth.hashers import make_password

# ========================
# USUARIO
# ========================
class Usuario(models.Model):
    ROLES = [
        ('Administrador', 'Administrador'),
        ('Supervisor', 'Supervisor'),
        ('Empleado', 'Empleado'),
    ]

    ESTADOS = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
        ('Incapacitado', 'Incapacitado'),
        ('Suspendido', 'Suspendido'),
    ]

    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    rol = models.CharField(max_length=20, choices=ROLES)
    estado = models.CharField(max_length=20, choices=ESTADOS)

    def __str__(self):
        return self.nombre


# ========================
# TURNO
# ========================
class Turno(models.Model):
    HORARIOS = [
        ('Mañana', 'Mañana 6:00am - 2:00pm'),
        ('Tarde', 'Tarde 2:00pm - 10:00pm'),
    ]

    fecha = models.DateField()
    horario = models.CharField(max_length=50, choices=HORARIOS)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.horario} - {self.fecha}"


# ========================
# ASIGNACION
# ========================
class Asignacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tarea = models.CharField(max_length=255)
    fecha_asignacion = models.DateField()
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario} - {self.turno}"


# ========================
# REPORTE
# ========================
class Reporte(models.Model):
    tipo = models.CharField(max_length=100)
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.tipo


# ========================
# PRODUCCION
# ========================
class Produccion(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Finalizado', 'Finalizado'),
    ]

    producto = models.CharField(max_length=100)
    ingredientes = models.TextField()
    cantidad_planificada = models.IntegerField()
    cantidad_producida = models.IntegerField(default=0)
    fecha_entrega = models.DateTimeField()
    fecha_limite = models.DateTimeField()
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    reporte = models.ForeignKey(Reporte, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.producto


# ========================
# EXPORTACION
# ========================
class Exportacion(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Enviado', 'Enviado'),
        ('Entregado', 'Entregado'),
    ]

    destino = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    fecha_envio = models.DateField(null=True, blank=True)
    fecha_entrega = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS)
    reporte = models.ForeignKey(Reporte, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.destino} - {self.pais}"


# ========================
# LOTE
# ========================
class Lote(models.Model):
    codigo_lote = models.CharField(max_length=100, unique=True)
    cantidad = models.IntegerField()
    fecha_produccion = models.DateField()
    fecha_vencimiento = models.DateField()

    produccion = models.ForeignKey(Produccion, on_delete=models.CASCADE)
    exportacion = models.ForeignKey(Exportacion, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.codigo_lote


