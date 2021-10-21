from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import Pacienteform, Contactform, PersonaForm
from .models import *
from django.contrib import messages
import io
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.platypus import Table, SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


# Create your views here.

#### LOGIN ####

def registroUsuario(request):
    if request.method == "POST":
        nombreUsuario = request.POST['nombreUsuario']
        Email = request.POST['correo']
        pwd = request.POST['password']
        Edad = request.POST['edad']
        Genero = request.POST['genero']
        Estado = request.POST['estado']
        nuevoUsuario(nombreUsuario=nombreUsuario, Email=Email, pwd=pwd, Edad=Edad, Genero=Genero, Estado=Estado).save()
        messages.success(request, 'El usuario' + request.POST['nombreUsuario'] + 'se registro exitosamente')
        return render(request, 'usuario/registrarse.html')
    else:
        return render(request, 'usuario/registrarse.html')


def paginalogin(request):
    if request.method == "POST":
        try:
            detalleUsuario = nuevoUsuario.objects.get(Email=request.POST['correo'], pwd=request.POST['password'])
            print("Usuario=", detalleUsuario)
            request.session['Email'] = detalleUsuario.Email
            return render(request, 'home.html')
        except nuevoUsuario.DoesNotExist as e:
            messages.success(request, 'Correo o Password no es correcto')
    return render(request, 'usuario/login.html')


#### CONTACTO ####

def contacto(request):
    contact_form = Contactform()
    if request.method == 'POST':
        contact_form = Contactform(data=request.POST)
        if contact_form.is_valid():
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            content = request.POST.get('content', '')
            # Creamos el correo
            email = EmailMessage(
                "El que no vive para servir no sirve para vivir",
                "de {} <{}>\n\nEscribio;\n\n{}".format(name, email, content),
                "no-contestar@inboxmailtrap.io",
                ["avtoledo@est.itsgg.edu.ec"],
                reply_to=[email]
            )
            # lo enviamos y redireccionamos
            try:
                email.send()
                # Todo ha salido Excelent, redireccionamos a OK
                return redirect(reverse('contacto') + "?okey")
            except:
                # Algo no ha salido bien, redireccionamos a FAIL
                return redirect(reverse('contacto') + "?fail")

            return redirect(reverse('contacto') + "?okey")
            # return redirect ('/contacto/?ok')
    return render(request, 'contacto.html', {'formulario': contact_form})


def inicio(request):
    return render(request, 'inicio.html')


def home(request):
    return render(request, 'home.html')


def pacientelistar(request):
    objpaciente = paciente.objects.all()
    return render(request, 'paciente/consultar_paciente.html', {'cargapcte': objpaciente})


def Guardarados2(request):
    return render(request, 'consultar_paciente.html')


def addpaciente(request):
    form = Pacienteform()

    if request.method == "POST":

        form = Pacienteform(request.POST)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            objpaciente = paciente.objects.all()

            return render(request, 'paciente/consultar_paciente.html', {'cargapcte': objpaciente})

    return render(request, 'paciente/crear_paciente.html', {'form': form})


def edit(request, id):
    # Recuperamos la instancia de la persona
    instancia = paciente.objects.get(id=id)

    # Creamos el formulario con los datos de la instancia
    form = Pacienteform(instance=instancia)

    # Comprobamos si se ha enviado el formulario
    if request.method == "POST":
        # Actualizamos el formulario con los datos recibidos
        form = Pacienteform(request.POST, instance=instancia)
        # Si el formulario es válido...
        if form.is_valid():
            # Guardamos el formulario pero sin confirmarlo,
            # así conseguiremos una instancia para manejarla
            instancia = form.save(commit=False)
            # Podemos guardarla cuando queramos
            instancia.save()
            objpaciente = paciente.objects.all()
            return render(request, 'paciente/consultar_paciente.html', {'cargapcte': objpaciente})

    # Si llegamos al final renderizamos el formulario
    return render(request, 'paciente/modificar_paciente.html', {'form': form})


def ver(request, id):
    objpaciente = paciente.objects.filter(id=id)
    return render(request, 'paciente/consultar_paciente.html', {'cargapcte': objpaciente})


def delete(request, id):
    # Recuperamos la instancia de la persona y la borramos

    instancia = paciente.objects.get(id=id)
    instancia.delete()

    # Después redireccionamos de nuevo a la lista
    objpaciente = paciente.objects.all()
    return render(request, 'paciente/consultar_paciente.html', {'cargapcte': objpaciente})


def buscapacient(request):
    if request.GET["pwd"]:
        # mensaje ="La categoria a buscar es  :%r" %request.GET["pwd"]
        pwd = request.GET["pwd"]
        doc = paciente.objects.filter(pacientecedula=pwd)
        return render(request, "paciente/consultar_paciente.html", {'cargapcte': doc})
    else:
        # mensaje = "Por favor ingrese la categoria a buscar :%r" % request.GET["pwd"]
        pwd = request.GET["pwd"]
        doc = paciente.objects.all()
        return render(request, "paciente/presentar_paciente.html")
        # return HttpResponse(mensaje)


def paciente_print(self, pk=None):
    response = HttpResponse(content_type='application/pdf')
    buff = io.BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=A4,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    lista = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Pacientes", styles['Heading1'])
    lista.append(header)
    headings = ('Fecha Registro', 'Fecha Modificacion', 'Cedula', 'Apellidos',
                'Nombre', 'Direccion', 'Estado')
    if not pk:
        todoslista = [(p.pacientefecharegistro, p.pacientefechamodificacion,
                       p.pacientecedula, p.pacienteapellido, p.pacientenombre
                       , p.pacientedireccion, p.pacienteestado)
                      for p in paciente.objects.all().order_by('pk')]
    else:
        todoslista = [(p.pacientefecharegistro, p.pacientefechamodificacion,
                       p.pacientecedula, p.pacienteapellido, p.pacientenombre
                       , p.pacientedireccion, p.pacienteestado)
                      for p in paciente.objects.filter(id=pk)]
    t = Table([headings] + todoslista)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (10, -1), 1, colors.dodgerblue),
            ('ALIGN', (0, 0), (3, 0), 'CENTER'),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
            ('LEFTPADDING', (0, 0), (-1, -1), -1),
            ('RIGHTPADDING', (0, 0), (-1, -1), 1),

        ]
    ))

    lista.append(t)
    doc.build(lista)
    response.write(buff.getvalue())
    buff.close()
    return response


#### CRUD DOCTOR ####

class doctorlistar(ListView):
    model = doctor
    template_name = 'doctor/doctor_listar.html'


class doctorcrear(CreateView):
    model = doctor
    fields = ['doctorcedula',
              'doctorregistro',
              'id_especialidad',
              'doctorapellido',
              'doctornombre',
              'doctordireccion',
              'doctorestado']
    template_name = 'doctor/doctor_crear.html'
    success_url = reverse_lazy('doctorlistar')


class doctormodificar(UpdateView):
    model = doctor
    fields = ['doctorcedula',
              'doctorregistro',
              'id_especialidad',
              'doctorapellido',
              'doctornombre',
              'doctordireccion',
              'doctorestado']
    template_name = 'doctor/doctor_modificar.html'
    success_url = reverse_lazy('doctorlistar')


class doctoreliminar(DeleteView):
    model = doctor
    template_name = 'doctor/doctor_eliminar.html'
    success_url = reverse_lazy('doctorlistar')


class doctorpresentar(DetailView):
    model = doctor
    template_name = 'doctor/doctor_presentar.html'


def buscadoc(request):
    if request.GET["pwd"]:
        # mensaje ="La categoria a buscar es  :%r" %request.GET["pwd"]
        pwd = request.GET["pwd"]
        doc = doctor.objects.filter(doctorcedula=pwd)
        return render(request, "doctor/doctor_presentar.html", {'doct': doc})
    else:
        # mensaje = "Por favor ingrese la categoria a buscar :%r" % request.GET["pwd"]
        pwd = request.GET["pwd"]
        doc = doctor.objects.all()
        return render(request, "doctor/doctor_presentar.html")
        # return HttpResponse(mensaje)


def doctor_print(self, pk=None):
    response = HttpResponse(content_type='application/pdf')
    buff = io.BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=A4,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    lista = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Doctores", styles['Heading1'])
    lista.append(header)
    headings = ('Fecha Registro', 'Fecha Modificacion', 'Id', 'Cedula', 'Apellidos',
                'Direccion', 'Estado')
    if not pk:
        todoslista = [(p.doctorfecharegistro, p.doctorfechamodificacion,
                       p.doctorcedula, p.doctorapellido, p.doctornombre
                       , p.doctordireccion, p.doctorestado)
                      for p in doctor.objects.all().order_by('pk')]
    else:
        todoslista = [(p.doctorfecharegistro, p.doctorfechamodificacion,
                       p.doctorcedula, p.doctorapellido, p.doctornombre
                       , p.doctordireccion, p.doctorestado)
                      for p in doctor.objects.filter(id=pk)]
    t = Table([headings] + todoslista)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (10, -1), 1, colors.dodgerblue),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))

    lista.append(t)
    doc.build(lista)
    response.write(buff.getvalue())
    buff.close()
    return response


#### CRUD CITA MEDICA ####

class cita_medicalistar(ListView):
    model = cita_medica
    template_name = 'cita_medica/cita_medicalistar.html'


class cita_medicacrear(CreateView):
    model = cita_medica
    fields = ['id_paciente',
              'id_doctor',
              'id_especialidad',
              'cita_medicacodigo',
              'cita_medicafecha',
              'cita_medicahora',
              'cita_medicaestado']
    template_name = 'cita_medica/cita_medicacrear.html'
    success_url = reverse_lazy('cita_medicalistar')


class cita_medicamofificar(UpdateView):
    model = cita_medica
    fields = ['id_paciente',
              'id_doctor',
              'id_especialidad',
              'cita_medicacodigo',
              'cita_medicafecha',
              'cita_medicahora',
              'cita_medicaestado']
    template_name = 'cita_medica/cita_medicamodificar.html'
    success_url = reverse_lazy('cita_medicalistar')


class cita_medicaeliminar(DeleteView):
    model = cita_medica
    template_name = 'cita_medica/cita_medicaeliminar.html'
    success_url = reverse_lazy('cita_medicalistar')


class cita_medicapresentar(DetailView):
    model = cita_medica
    template_name = 'cita_medica/cita_medica_presentar.html'


def cita_med_print(self, pk=None):
    response = HttpResponse(content_type='application/pdf')
    buff = io.BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=landscape(A4),
                            rightMargin=40,
                            leftMargin=20,
                            topMargin=60,
                            bottomMargin=18,
                            )

    lista = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Citas", styles['Heading1'])
    lista.append(header)
    headings = ('Fecha Registro', 'Fecha Modificacion', 'Id', 'Codigo Especialidad', 'Doctor',
                'Paciente', 'Especialidad', 'Fecha Cita', 'Hora Cita', 'Estado')
    if not pk:

        todoslista = [(p.cita_medicaregistro, p.cita_medicamodificacion, p.id,
                       p.cita_medicacodigo, p.id_paciente, p.id_doctor
                       , p.id_especialidad, p.cita_medicafecha, p.cita_medicahora, p.cita_medicaestado)
                      for p in cita_medica.objects.all().order_by('pk')]
    else:
        todoslista = [(p.cita_medicaregistro, p.cita_medicamodificacion, p.id,
                       p.cita_medicacodigo, p.id_paciente, p.id_doctor
                       , p.id_especialidad, p.cita_medicafecha, p.cita_medicahora, p.cita_medicaestado)
                      for p in cita_medica.objects.filter(id=pk)]

    t = Table([headings] + todoslista)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (10, -1), 1, colors.dodgerblue),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('LEFTPADDING', (0, 0), (-1, -1), -1),
            ('RIGHTPADDING', (0, 0), (-1, -1), 1),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))

    lista.append(t)
    doc.build(lista)
    response.write(buff.getvalue())
    buff.close()
    return response


def buscacitamed(request):
    if request.GET["pwd"]:
        # mensaje ="La categoria a buscar es  :%r" %request.GET["pwd"]
        pwd = request.GET["pwd"]
        doc = cita_medica.objects.filter(cita_medicacodigo=pwd)
        return render(request, "cita_medica/cita_medicapresentar.html", {'doct': doc})
    else:
        # mensaje = "Por favor ingrese la categoria a buscar :%r" % request.GET["pwd"]
        pwd = request.GET["pwd"]
        doc = cita_medica.objects.all()
        return render(request, "cita_medica/cita_medicapresentar.html")
        # return HttpResponse(mensaje)


### CRUD especialidad ####

class especialidadlistar(ListView):
    model = especialidad
    template_name = 'especialidad/especialidad_listar.html'


class especialidadcrear(CreateView):
    model = especialidad
    fields = ['especialidadnombre',
              'especialidadestado']
    template_name = 'especialidad/especialidad_crear.html'
    success_url = reverse_lazy('especialidadlistar')


class especialidadmofificar(UpdateView):
    model = especialidad
    fields = ['especialidadnombre',
              'especialidadestado']
    template_name = 'especialidad/especialidad_modificar.html'
    success_url = reverse_lazy('especialidadlistar')


class especialidadeliminar(DeleteView):
    model = especialidad
    template_name = 'especialidad/especialidad_eliminar.html'
    success_url = reverse_lazy('especialidadlistar')


class especialidadpresentar(DetailView):
    model = especialidad
    template_name = 'especialidad/especialidad_presentar.html'


def especialidad_print(self, pk=None):
    response = HttpResponse(content_type='application/pdf')
    buff = io.BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=A4,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )

    lista = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Especialidad", styles['Heading1'])
    lista.append(header)
    headings = ('Fecha Registro', 'Fecha Modificacion', 'Id', 'Especialidad', 'Estado')
    if not pk:

        todoslista = [(p.especialidadfecharegistro, p.especialidadfechamodificacion, p.id,
                       p.especialidadnombre, p.especialidadestado)
                      for p in especialidad.objects.all().order_by('pk')]
    else:
        todoslista = [(p.especialidadfecharegistro, p.especialidadfechamodificacion, p.id,
                       p.especialidadnombre, p.especialidadestado)
                      for p in especialidad.objects.filter(id=pk)]

    t = Table([headings] + todoslista)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (10, -1), 1, colors.dodgerblue),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))

    lista.append(t)
    doc.build(lista)
    response.write(buff.getvalue())
    buff.close()
    return response


def buscaespecialidad(request):
    if request.GET["pwd"]:
        # mensaje ="La categoria a buscar es  :%r" %request.GET["pwd"]
        pwd = request.GET["pwd"]
        doc = especialidad.objects.filter(especialidadnombre=pwd)
        return render(request, "especialidad/especialidad_presentar.html", {'doct': doc})
    else:
        # mensaje = "Por favor ingrese la categoria a buscar :%r" % request.GET["pwd"]
        pwd = request.GET["pwd"]
        doc = especialidad.objects.all()
        return render(request, "especialidad/especialidad_presentar.html")
        # return HttpResponse(mensaje)

################# CRUD FICHA MEDICA  #######################

class ficha_medica_listar(ListView):
    model = ficha_medica
    template_name = 'ficha_medica/ficha_medica_listar.html'


class ficha_medica_crear(CreateView):
    model = ficha_medica
    fields = ['ficha_medica_codigo','id_especialidad','id_cita_medica','id_paciente','id_doctor',
             'ficha_medica_diagnostico','ficha_medica_tratamiento','ficha_medica_estado'
              ]
    template_name = 'ficha_medica/ficha_medica_crear.html'
    success_url = reverse_lazy('ficha_medica_listar')


class ficha_medica_modificar(UpdateView):
    model = ficha_medica
    fields = ['ficha_medica_codigo','id_especialidad','id_cita_medica','id_paciente','id_doctor',
             'ficha_medica_diagnostico','ficha_medica_tratamiento','ficha_medica_estado'
              ]
    template_name = 'ficha_medica/ficha_medica_modificar.html'
    success_url = reverse_lazy('ficha_medica_listar')


class ficha_medica_eliminar(DeleteView):
    model = ficha_medica
    template_name = 'ficha_medica/ficha_medica_eliminar.html'
    success_url = reverse_lazy('ficha_medica_listar')


class ficha_medica_presentar(DetailView):
    model = ficha_medica
    template_name = 'ficha_medica/ficha_medica_presentar.html'


def busca_ficha_medica(request):
    if request.GET["pwd"]:
        pwd = request.GET["pwd"]
        doc = ficha_medica.objects.filter(ficha_medica_codigo=pwd)
        return render(request, "ficha_medica/ficha_medica_presentar.html", {'doct': doc})
    else:
        pwd = request.GET["pwd"]
        doc = ficha_medica.objects.all()
        return render(request, "ficha_medica/ficha_medica_presentar.html")


def ficha_medica_print(self, pk=None):
    response = HttpResponse(content_type='application/pdf')
    buff = io.BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=landscape(A4),
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )

    lista = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Fichamedica", styles['Heading1'])
    lista.append(header)
    headings = ('Fecha Registro', 'Fecha Modificacion', 'Id', 'Codigo Cita Medica','Paciente', 'Doctor', 'Especialidad',
                'Cita Medica', 'Diagnostico','Tratamiento', 'Estado')
    if not pk:

        todoslista = [(p.ficha_medica_registro,p.ficha_medica_modificacion,p.id,p.ficha_medica_codigo,p.id_paciente,p.id_doctor,
                       p.id_especialidad,p.id_cita_medica,p.ficha_medica_diagnostico,p.ficha_medica_tratamiento,
                       p.ficha_medica_estado)
                      for p in ficha_medica.objects.all().order_by('pk')]
    else:
        todoslista = [(p.ficha_medica_registro,p.ficha_medica_modificacion,p.id,p.ficha_medica_codigo,p.id_paciente,p.id_doctor,
                       p.id_especialidad,p.id_cita_medica,p.ficha_medica_diagnostico,p.ficha_medica_tratamiento,
                       p.ficha_medica_estado)
                      for p in ficha_medica.objects.filter(id=pk)]

    t = Table([headings] + todoslista)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (10, -1), 1, colors.dodgerblue),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('LEFTPADDING', (0, 0), (-1, -1), -1),
            ('RIGHTPADDING', (0, 0), (-1, -1), 1),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))

    lista.append(t)
    doc.build(lista)
    response.write(buff.getvalue())
    buff.close()
    return response



#### CRUD  PERSONA ###

def consultar_persona(request):
    personas = Persona.objects.all()
    return render(request, "persona/consultar_persona.html", {'personas_ls': personas})


def crear_persona(request):
    if request.method == "POST":
        personaForm = PersonaForm(request.POST)
        if personaForm.is_valid():
            personaForm.save()
            return redirect('consultar_persona')
        else:
            personaForm = PersonaForm()
    else:
        personaForm = PersonaForm()
    return render(request, "persona/crear_persona.html", {'personaForm': personaForm})


def eliminar_persona(request, id):
    if request.method == "POST":
        persona = get_object_or_404(Persona, pk=id)
        personaForm = PersonaForm(request.POST or None, instance=persona)
        if personaForm.is_valid():
            persona.estado = 0
            persona.save()
            ##personaForm.
            return redirect('consultar_persona')
    else:  ##GET
        persona = get_object_or_404(Persona, pk=id)
        personaForm = PersonaForm(instance=persona)
    return render(request, "persona/eliminar_persona.html", {'personaForm': personaForm})


def modificar_persona(request, id):
    if request.method == "POST":
        persona = get_object_or_404(Persona, pk=id)
        personaForm = PersonaForm(request.POST or None, instance=persona)
        if personaForm.is_valid():
            personaForm.save()
            return redirect('consultar_persona')
        else:
            personaForm = PersonaForm(instance=persona)
    else:  ##GET
        persona = get_object_or_404(Persona, pk=id)
        personaForm = PersonaForm(instance=persona)
    return render(request, "persona/modificar_persona.html", {'personaForm': personaForm})
