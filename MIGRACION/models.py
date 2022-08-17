from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class seguimiento(models.Model):
    NUMERO_DOCUMENTO=models.CharField(max_length=30)
    ID_ACTIVIDAD=models.CharField(max_length=30)
    ID_CURSO_DE_VIDA=models.CharField(max_length=30)
    EDAD=models.CharField(max_length=30)   

class Actividad(models.Model):
    ID_ACTIVIDAD=models.CharField(max_length=120)
    NOMBRE_ACTIVIDAD=models.CharField(max_length=120)
    ID_INDICADOR=models.CharField(max_length=30)
    class Meta:
        managed = False
        db_table = 'ACTIVIDAD'
      
    

class SeguimientoNominalNinio(models.Model):    
    ID = models.BigIntegerField(primary_key=True)
    numero_documento = models.CharField(db_column='NUMERO_DOCUMENTO', max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    Fecha_Nacimiento_Paciente = models.CharField(db_column='Fecha_Nacimiento_Paciente', max_length=250, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    Apellido_Paterno_Paciente = models.CharField(db_column='Apellido_Paterno_Paciente', max_length=250, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    Apellido_Materno_Paciente = models.CharField(db_column='Apellido_Materno_Paciente', max_length=250, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    Nombres_Paciente = models.CharField(db_column='Nombres_Paciente', max_length=250, db_collation='Modern_Spanish_CI_AS', blank=True, null=True) 
    IPRESS = models.CharField(db_column='IPRESS', max_length=250, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)      
    id_actividad = models.IntegerField(db_column='id_ACTIVIDAD')  # Field name made lowercase.
    id_curso_de_vida = models.IntegerField(db_column='id_CURSO_DE_VIDA')  # Field name made lowercase.
    edad = models.IntegerField(db_column='EDAD', blank=True, null=True)  # Field name made lowercase.
    tipo_edad = models.CharField(db_column='TIPO_EDAD', max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    renipress = models.CharField(max_length=12, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    cumple = models.CharField(db_column='CUMPLE', max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mes = models.IntegerField(db_column='MES', blank=True, null=True)  # Field name made lowercase.
    anio = models.IntegerField(blank=True, null=True)
    id_indicador = models.IntegerField(db_column='id_INDICADOR', blank=True, null=True)  # Field name made lowercase.
    fecha_atencion = models.DateField(db_column='Fecha_Atencion', blank=True, null=True)  # Field name made lowercase.
    id_cita = models.CharField(db_column='Id_cita', max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SEGUIMIENTO_NOMINAL_VIEW_T'