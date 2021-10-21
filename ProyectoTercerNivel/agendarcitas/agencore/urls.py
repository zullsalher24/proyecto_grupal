from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
#from .views import doctorlistar, doctorcrear, doctorpresentar, doctormodificar, doctoreliminar
from .views import *


urlpatterns = [

    path('inicio', views.inicio, name='inicio'),
    path('home', views.home, name='home'),

    #######################  LOGIN  #####################

    path('reg', views.registroUsuario, name='reg'),
    path('', views.paginalogin, name='paginalogin'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login.html'), name='logout'),

    #######################  PACIENTE #####################
    path('pacientelistar', views.pacientelistar, name='pacientelistar'),
    path('pacienteaguardar/', views.addpaciente, name='pacienteaguardar'),
    path('pacientemodificar/edit/<int:id>', views.edit, name='pacientemodificar'),
    path('pacientever/ver/<int:id>', views.ver, name='pacientever'),
    path('pacienteeliminar/delete/<int:id>', views.delete, name='pacienteeliminar'),
    path('pacienteindividual/<int:pk>', views.paciente_print, name='pacienteindividual'),
    path('pacientepdf', views.paciente_print, name='pacientepdf'),
    path('buscar1/', views.buscapacient),

    ######################  DOCTOR   ######################
    path('doctorlistar', views.doctorlistar.as_view(), name='doctorlistar'),
    path('doctormodificar/<int:pk>', views.doctormodificar.as_view(), name='doctormodificar'),
    path('doctorcrear/', doctorcrear.as_view(), name='doctorcrear'),
    path('doctoreliminar/<int:pk>', doctoreliminar.as_view(), name='doctoreliminar'),
    path('doctorpresentar/<int:pk>/<slug:slug>/', doctorpresentar.as_view(), name='doctorpresentar'),
    path('doctorver/ver/<int:id>', views.ver, name='doctorever'),
    path('doctorindivpdf/<int:pk>', views.doctor_print, name='doctorindivpdf'),
    path('doctorpdf', views.doctor_print, name='doctorpdf'),
    path('buscar/', views.buscadoc),

    #################### CONTACTO #########################

    path('contacto', views.contacto, name='contacto'),

    ####  CITA MEDICA ####

    path('cita_medicalistar', views.cita_medicalistar.as_view(), name='cita_medicalistar'),
    path('cita_medicacrear', views.cita_medicacrear.as_view(), name='cita_medicacrear'),
    path('cita_medicamodificar/<int:pk>', views.cita_medicamofificar.as_view(), name='cita_medicamofificar'),
    path('cita_medicaeliminar/<int:pk>', cita_medicaeliminar.as_view(), name='cita_medicaeliminar'),
    path('cita_medicapresentar/<int:pk>/<slug:slug>/', cita_medicapresentar.as_view(), name='cita_medicapresentar'),
    path('cita_medicaver/ver/<int:id>', views.ver, name='cita_medicaever'),
    path('cita_medindivpdf/<int:pk>', views.cita_med_print, name='cita_medindivpdf'),
    path('cita_medicapdf', views.cita_med_print, name='cita_medicapdf'),
    path('buscar2/', views.buscacitamed),

    ######################  ESPECIALIDAD  ######################
    path('eespecialidadlistar', especialidadlistar.as_view(), name='especialidadlistar'),
    path('especialidadmodificar/<int:pk>', views.especialidadmofificar.as_view(), name='especialidadmodificar'),
    path('especialidadcrear/', especialidadcrear.as_view(), name='especialidadcrear'),
    path('especialidadeliminar/<int:pk>', especialidadeliminar.as_view(), name='especialidadeliminar'),
    path('especialidadpresentar/<int:pk>/<slug:slug>/', especialidadpresentar.as_view(), name='especialidadpresentar'),
    path('especialidadver/ver/<int:id>', views.ver, name='especialidadever'),
    path('especialidadindivpdf/<int:pk>', views.especialidad_print, name='especialidadindivpdf'),
    path('especialidadpdf', views.especialidad_print, name='especialidadpdf'),
    path('buscar3/', views.buscaespecialidad),


    ######################  FICHA_MEDICA   ######################

    path('ficha_medica_listar', views.ficha_medica_listar.as_view(), name='ficha_medica_listar'),
    path('ficha_medica_modificar/<int:pk>', views.ficha_medica_modificar.as_view(), name='ficha_medica_modificar'),
    path('ficha_medica_crear/', views.ficha_medica_crear.as_view(), name='ficha_medica_crear'),
    path('ficha_medica_eliminar/<int:pk>', views.ficha_medica_eliminar.as_view(), name='ficha_medica_eliminar'),
    path('ficha_medica_presentar/<int:pk>/<slug:slug>/', views.ficha_medica_presentar.as_view(),
         name='ficha_medica_presentar'),
    path('ficha_medica_ver/ver/<int:id>', views.ver, name='ficha_medica_ver'),
    path('ficha_medicaindivpdf/<int:pk>', views.ficha_medica_print, name='ficha_medicaindivpdf'),
    path('ficha_medicapdf', views.ficha_medica_print, name='ficha_medicapdf'),
    path('buscar4/', views.busca_ficha_medica),








    # RUTAS PARA EL CRUD DE LA ENTIDAD PERSONA#
    path('consultar_persona/', views.consultar_persona, name='consultar_persona'),
    path('crear_persona/', views.crear_persona, name='crear_persona'),
    path('eliminar_persona/<int:id>', views.eliminar_persona, name='eliminar_persona'),
    path('modificar_persona/<int:id>', views.modificar_persona, name='modificar_persona'),




]
