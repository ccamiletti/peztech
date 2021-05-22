from django.db import models
import json
import jsonpickle

# Create your models here.
class Modulo(models.Model):
    moduloNumero = models.IntegerField(unique=True, null=False)
    moduloDescription = models.TextField()


class JsonTransformer(object):
    def transform(self, myObject):
        return jsonpickle.encode(myObject, unpicklable=False)
    
class Jaula(models.Model):
    modulo = models.ForeignKey(
        Modulo, null=False, blank=False, on_delete=models.CASCADE)
    jaulaNumero = models.IntegerField(unique=True, null=False)


class JaulaView:
    def __init__(self, id_jaula, jaulaNumero, numero_modulo, modulo_id):
        self.id_jaula = id_jaula
        self.jaulaNumero = jaulaNumero
        self.numero_modulo = numero_modulo
        self.modulo_id = modulo_id


    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                      sort_keys=True)

class Centro(models.Model):
    nombre = models.TextField(max_length=200)
    rangoHorarioDesde = models.IntegerField()
    rangoHorarioHasta = models.IntegerField()
    diasAlmacenamientoStream = models.IntegerField()
    canalStream = models.TextField(max_length=100)
    smtpHost = models.TextField(max_length=100)
    smtpUsuario = models.TextField(max_length=100)
    smtpContrasena = models.TextField(max_length=100)
    smtpSecure = models.TextField(max_length=50)
    smtpPuerto = models.IntegerField()


class CentroDestinatario(models.Model):
    centro = models.ForeignKey(
        Centro, null=False, blank=False, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)


class RecordHistory(models.Model):
    startTime = models.TextField(max_length=50)
    endTime = models.TextField(max_length=50)
    observation = models.TextField(max_length=2000)
    statusRecord = models.TextField(max_length=50)
    saveVideo = models.CharField(max_length=1)
    obsNameVideo = models.TextField(max_length=200)
    statusUpload = models.CharField(max_length=50)
    dateUpload = models.CharField(max_length=50)
