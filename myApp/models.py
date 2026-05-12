from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    ROL_CHOICES = [('Administrador', 'Administrador'), ('Supervisor', 'Supervisor')]
    ESTADO_CHOICES = [('Activo', 'Activo'), ('Inactivo', 'Inactivo'),
                      ('Incapacitado', 'Incapacitado'), ('Suspendido', 'Suspendido')]
    nombre     = models.CharField(max_length=100, null=True, blank=True)
    email      = models.EmailField(unique=True, max_length=255)
    telefono   = models.IntegerField(null=True, blank=True)
    direccion  = models.CharField(max_length=255, null=True, blank=True)
    contrasena = models.CharField(max_length=255, null=True, blank=True)
    rol        = models.CharField(max_length=20, choices=ROL_CHOICES, null=True, blank=True)
    estado     = models.CharField(max_length=20, choices=ESTADO_CHOICES, null=True, blank=True)
    def __str__(self): return self.nombre or ''

class Empleado(models.Model):
    ESTADO_CHOICES = [('Activo', 'Activo'), ('Inactivo', 'Inactivo'),
                      ('Incapacitado', 'Incapacitado'), ('Suspendido', 'Suspendido')]
    cedula    = models.CharField(max_length=20, null=True, blank=True)
    nombre    = models.CharField(max_length=100, null=True, blank=True)
    email     = models.EmailField(unique=True, max_length=255)
    telefono  = models.IntegerField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    estado    = models.CharField(max_length=20, choices=ESTADO_CHOICES, null=True, blank=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL,
                    null=True, blank=True, db_column='creado_por')
    def __str__(self): return self.nombre or ''

class Turno(models.Model):
    HORARIO_CHOICES = [('Mañana 6:00am - 2:00pm', 'Mañana 6:00am - 2:00pm'),
                       ('Tarde 2:00pm - 10:00pm', 'Tarde 2:00pm - 10:00pm')]
    fecha   = models.DateField(null=True, blank=True)
    horario = models.CharField(max_length=50, choices=HORARIO_CHOICES, null=True, blank=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL,
                    null=True, blank=True, db_column='creado_por')
    def __str__(self): return f"{self.fecha} - {self.horario}"

class EmpTurno(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL,
                    null=True, blank=True, db_column='empleado_id')
    turno    = models.ForeignKey(Turno, on_delete=models.SET_NULL,
                    null=True, blank=True, db_column='turno_id')
    def __str__(self): return f"{self.empleado} - {self.turno}"

class Asignacion(models.Model):
    tarea            = models.CharField(max_length=255, null=True, blank=True)
    fecha_asignacion = models.DateField(null=True, blank=True)
    empleado     = models.ForeignKey(Empleado, on_delete=models.SET_NULL,
                      null=True, blank=True, db_column='empleado_id')
    turno        = models.ForeignKey(Turno, on_delete=models.SET_NULL,
                      null=True, blank=True, db_column='turno_id')
    asignado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL,
                      null=True, blank=True, db_column='asignado_por')
    def __str__(self): return f"{self.tarea} - {self.empleado}"

class Produccion(models.Model):
    ESTADO_CHOICES = [('Pendiente','Pendiente'),('En Proceso','En Proceso'),
                      ('Cancelado','Cancelado'),('Finalizado','Finalizado')]
    producto             = models.CharField(max_length=255, null=True, blank=True)
    ingredientes         = models.CharField(max_length=255, null=True, blank=True)
    cantidad_planificada = models.CharField(max_length=255, null=True, blank=True)
    cantidad_producida   = models.CharField(max_length=255, null=True, blank=True)
    fecha_entrega        = models.DateField(null=True, blank=True)
    fecha_limite         = models.DateField(null=True, blank=True)
    fecha_inicio         = models.DateField(null=True, blank=True)
    fecha_fin            = models.DateField(null=True, blank=True)
    estado               = models.CharField(max_length=20, choices=ESTADO_CHOICES, null=True, blank=True)
    empleado_responsable = models.ForeignKey(Empleado, on_delete=models.SET_NULL,
                              null=True, blank=True, db_column='empleado_responsable')
    creado_por           = models.ForeignKey(Usuario, on_delete=models.SET_NULL,
                              null=True, blank=True, db_column='creado_por')
    def __str__(self): return f"{self.producto} - {self.estado}"

class Exportacion(models.Model):
    ESTADO_CHOICES = [('Pendiente','Pendiente'),('Enviado','Enviado'),
                      ('Entregado','Entregado'),('Cancelado','Cancelado')]
    destino       = models.CharField(max_length=255, null=True, blank=True)
    pais          = models.CharField(max_length=255, null=True, blank=True)
    fecha_envio   = models.DateField(null=True, blank=True)
    fecha_entrega = models.DateField(null=True, blank=True)
    estado        = models.CharField(max_length=20, choices=ESTADO_CHOICES, null=True, blank=True)
    creado_por    = models.ForeignKey(Usuario, on_delete=models.SET_NULL,
                      null=True, blank=True, db_column='creado_por')
    def __str__(self): return f"{self.destino} - {self.estado}"

class Lote(models.Model):
    codigo_lote       = models.CharField(max_length=100, unique=True)
    cantidad          = models.IntegerField(null=True, blank=True)
    fecha_produccion  = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    produccion  = models.ForeignKey(Produccion, on_delete=models.SET_NULL,
                     null=True, blank=True, db_column='produccion_id')
    exportacion = models.ForeignKey(Exportacion, on_delete=models.SET_NULL,
                     null=True, blank=True, db_column='exportacion_id')
    def __str__(self): return self.codigo_lote