"""pezTech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from pezInterface.views import \
    index, iniciarSeleccion, iniciar, finalizar, \
    modulos_list, modulo_view, modulo_edit, modulo_delete, centro_list, \
    jaulas_list, jaula_view, jaula_delete, jaulas_list_ajax, \
    centro_edit, centro_view, \
    testWS, otros_list, cierre_confirmacion, cierre_forzado_process, grabaciones_pendientes_list, \
    enviar_notificacion, proceso_carga_confirmacion, enviar_email, cargar_video, bienvenida, getJaulaByVoice

app_name = 'pezInterface'

urlpatterns = [
    path('', index, name='index'),
    path('iniciarSeleccion/', iniciarSeleccion, name='iniciar_seleccion'),
    path('bienvenida/', bienvenida, name='bienvenida'),
    path('getJaulaByVoice/', getJaulaByVoice, name='getJaulaByVoice'),

    path('iniciar/', iniciar, name='iniciar'),
    path('finalizar/', finalizar, name='finalizar'),
    path('modulos/', modulos_list, name='modulos_listar'),
    path('modulos/nuevo', modulo_view, name='modulos_nuevo'),
    path('modulos/editar/<int:id_modulo>', modulo_edit, name='modulos_editar'),
    path('modulos/eliminar/<int:id_modulo>',
         modulo_delete, name='modulos_eliminar'),
    path('modulos/jaulas/<int:id_modulo>', jaulas_list, name='jaulas_listar'),
    path('modulos/ajax/jaulas/', jaulas_list_ajax, name='jaulas_listar_ajax'),
    path('modulos/jaulas/nuevo/<int:id_modulo>',
         jaula_view, name='jaulas_nuevo'),
    path('modulos/jaulas/eliminar/<int:id_jaula>',
         jaula_delete, name='jaulas_eliminar'),
    path('centro/', centro_list, name='centro_listar'),
    path('centro/nuevo', centro_view, name='centro_nuevo'),
    path('centro/editar/<int:id_centro>', centro_edit, name='centro_editar'),
    path('ws/', testWS, name='ws'),
    path('otros/', otros_list, name='otros'),
    path('otros/cierre_confirmacion',
         cierre_confirmacion, name='cierre_confirmacion'),
    path('otros/grabaciones_pendientes',
         grabaciones_pendientes_list, name='grabaciones_pendientes'),
    path('otros/enviar_notificacion/<int:id_record>',
         enviar_notificacion, name='enviar_notificacion'),
    path('otros/proceso_carga_confirmacion/<int:id_record>',
         proceso_carga_confirmacion, name='proceso_carga_confirmacion'),
    path('otros/enviar_email', enviar_email, name='enviar_email'),
    path('otros/cargar_video', cargar_video, name='cargar_video'),
    path('otros/cierre_forzado', cierre_forzado_process, name='cierre_forzado'),
]

# path('modulos/nuevo', ModuloCreate.as_view(), name='modulos_nuevo'),
