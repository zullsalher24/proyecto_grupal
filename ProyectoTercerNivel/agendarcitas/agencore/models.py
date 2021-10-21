from django.db import models


# Create your models here.

class nuevoUsuario(models.Model):
    nombreUsuario = models.CharField(max_length=150)
    Email = models.CharField(max_length=150)
    pwd = models.CharField(max_length=150)
    Edad = models.IntegerField()
    Genero = models.CharField(max_length=1)
    Estado = models.CharField(max_length=150)


class especialidad(models.Model):
    especialidadfecharegistro = models.DateField(auto_now=False, auto_now_add=True)
    especialidadfechamodificacion = models.DateField(auto_now=False, auto_now_add=True)
    especialidadnombre = models.CharField(max_length=50)
    Estado = (
        ('1', 'Activo'),
        ('0', 'No Activo'),
    )
    especialidadestado = models.CharField(max_length=1, choices=Estado, default='1')

    def __str__(self):
        return self.especialidadnombre


class paciente(models.Model):
    pacientefecharegistro = models.DateField(auto_now=False, auto_now_add=True)
    pacientefechamodificacion = models.DateField(auto_now=False, auto_now_add=True)
    pacientecedula = models.CharField(max_length=10)
    pacienteapellido = models.CharField(max_length=30)
    pacientenombre = models.CharField(max_length=30)
    pacientedireccion = models.CharField(max_length=30)
    Estado = (
        ('1', 'Activo'),
        ('0', 'No Activo'),
    )
    pacienteestado = models.CharField(max_length=1,choices=Estado,default='1')

    def __str__(self):
        #return self.pacienteapellido
        cadena= self.pacienteapellido+" "+self.pacientenombre
        return cadena


class doctor(models.Model):
    doctorfecharegistro = models.DateField(auto_now=False, auto_now_add=True)
    doctorfechamodificacion = models.DateField(auto_now=False, auto_now_add=True)
    id_especialidad = models.ForeignKey(especialidad, on_delete=models.CASCADE)
    doctorcedula = models.CharField(max_length=10)
    doctorregistro = models.CharField(max_length=10)
    doctorapellido = models.CharField(max_length=30)
    doctornombre = models.CharField(max_length=30)
    doctordireccion = models.CharField(max_length=30)
    Estado = (
        ('1', 'Activo'),
        ('0', 'No Activo'),
    )
    doctorestado = models.CharField(max_length=1,choices=Estado,default='1')

    def __str__(self):
        #return self.doctorapellido
        cadena = self.doctorapellido + " " + self.doctornombre
        return cadena


class cita_medica(models.Model):
    id_paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    id_doctor = models.ForeignKey(doctor, on_delete=models.CASCADE)
    id_especialidad = models.ForeignKey(especialidad, on_delete=models.CASCADE)
    cita_medicacodigo= models.CharField(max_length=10)
    cita_medicaregistro = models.DateField(auto_now_add=True,blank=True, null=True)
    cita_medicamodificacion = models.DateField(auto_now_add=True,blank=True, null=True)
    cita_medicafecha = models.DateField()
    cita_medicahora = models.TimeField()
    Estado = (
        ('1', 'Activo'),
        ('0', 'No Activo'),
    )
    cita_medicaestado = models.CharField(max_length=1,choices=Estado,default='1')

    def __str__(self):
        #return self.cita_medicapaciente
        return '{}'.format(self.cita_medicacodigo)


class rol(models.Model):
    rolnombre = models.CharField(max_length=50)
    rolestado = models.IntegerField(default=1)

    def __str__(self):
        return self.rolnombre


class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=100)
    edad = models.CharField(max_length=3)
    direccion = models.CharField(max_length=255)
    cedula = models.CharField(max_length=10)
    correo = models.EmailField(null=True, blank=True)

    usuario_creacion = models.CharField(max_length=15)
    usuario_modificacion = models.CharField(max_length=15)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.IntegerField(default=1)

    def __str__(self):
        return "{}{}{}".format(self.apellido, " ", self.nombre)


class ficha_medica(models.Model):
    id_paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    id_doctor = models.ForeignKey(doctor, on_delete=models.CASCADE)
    id_especialidad = models.ForeignKey(especialidad, on_delete=models.CASCADE)
    id_cita_medica = models.ForeignKey(cita_medica, on_delete=models.CASCADE)
    ficha_medica_registro = models.DateField(auto_now_add=True,blank=True, null=True)
    ficha_medica_modificacion = models.DateField(auto_now_add=True,blank=True, null=True)
    ficha_medica_codigo=models.IntegerField(default=0)
    ficha_medica_diagnostico =models.CharField(max_length=150)
    ficha_medica_tratamiento =models.CharField(max_length=150)
    Estado = (
        ('1', 'Activo'),
        ('0', 'No Activo'),
    )
    ficha_medica_estado = models.CharField(max_length=1, choices=Estado, default='1')

    def __str__(self):
        return "{}".format(self.ficha_medica_codigo)

