from django.shortcuts import render
from tkinter.ttk import Separator
from django.shortcuts import render
from .models import Actividad, SeguimientoNominalNinio
from django.http import JsonResponse
from django.views import View
import happybase as hb
import os

# Create your views here.


class migracion_con(View):
    separador='$'
    
    def get(self,request,agnio,mes,id_curso):
        print(id_curso)
        anio = agnio
        mes = mes
        connection={}
        periodo=str(int(anio)*100+int(mes))
        nombre_curso=''
        indicador_min=0
        indicador_max=199
        if id_curso=='1':
            nombre_curso='MATERNO'
            indicador_min=0
            indicador_max=100

        if id_curso=='2':
            nombre_curso='NINIO'
            indicador_min=200
            indicador_max=299
            print(nombre_curso)
        if id_curso=='3':
            nombre_curso='ADOLECENTE'
            indicador_min=300
            indicador_max=399
        if id_curso=='4':
            nombre_curso='JOVEN'
            indicador_min=400
            indicador_max=499
        if id_curso=='5':
            nombre_curso='ADULTO'
            indicador_min=500
            indicador_max=599
        if id_curso=='6':
            nombre_curso='ADULTO_MAYOR'
            indicador_min=600
            indicador_max=699
        print(nombre_curso)
       
        print(str(int(anio)*100+int(mes)))
        
       
        '''
        lis_u=lista.values('id_actividad','id_indicador').distinct()

        dic={}

        for item in lis_u.values('id_actividad','id_indicador').distinct():
            print(item['id_actividad'])
            dic[str(item['id_indicador'])+'_'+str(item['id_actividad'])]={}
        
        print(dic)
        '''               
        print(periodo)
        self.crea_tabla(period=periodo,nombre_curs=nombre_curso)
        
        
        lista=SeguimientoNominalNinio.objects.filter(anio=agnio,mes=mes,id_curso_de_vida=id_curso)
        actividad=Actividad.objects.filter()
        
        print('taamanio')
      
        for item in lista.values():
            dicres={}
                    
            dicres['CMI_2022:ipress_adscripcion']=item['IPRESS']            
            dicres['CMI_2022:renipress_adscripcion']=item['renipress']
           
            dicres['CMI_2022:Apellido_Paterno_Paciente']=item['Apellido_Paterno_Paciente']
            dicres['CMI_2022:Apellido_Materno_Paciente']=item['Apellido_Materno_Paciente']
            dicres['CMI_2022:Nombres_Paciente']=item['Nombres_Paciente']
            
            if(item['fecha_atencion'] is None):
                item['fecha_atencion']=''
            else :
                item['fecha_atencion']=item['fecha_atencion'].strftime('%d-%m-%Y')
            
            if(item['id_cita'] is None):
                item['id_cita']=''
            else :
                item['id_cita']=item['id_cita']
            
            if(item['id_indicador'] is None):
                item['id_indicador']=''
            else :
                item['id_indicador']=item['id_indicador']            
            
            dicres['CMI_2022:'+str(item['id_indicador'])+self.separador+str(item['id_actividad'])+self.separador+'fecha_atencion']=item['fecha_atencion']
            
            dicres['CMI_2022:'+str(item['id_indicador'])+self.separador+str(item['id_actividad'])+self.separador+'cumple']=item['cumple']
           
            dicres['CMI_2022:'+str(item['id_indicador'])+self.separador+str(item['id_actividad'])+self.separador+'id_cita']=item['id_cita']
            try:
                connection=self.crea_coneccion()
                table_i= connection.table('PERIODO_'+str(periodo)+':SEGUIMIENTO_'+nombre_curso)
                table_i.put(item['numero_documento'],dicres)
               
                connection.close()
            except Exception as e:
                print('error '+str(item['numero_documento']))
                print(e)
 
                
        
        print(dicres.values())      
         
           
        return JsonResponse(list(lista.values()),safe=False)
    
    def crea_coneccion(self):
        try:
            con=  hb.Connection(os.environ.get('SERVER_HBASE'),port=int(os.environ.get('PORT_HBASE')) )
            con.open()
            return con
        except Exception as e:
            print(e)
            print('fallo la conneccion')
    def crea_tabla(self,period,nombre_curs):
        try:
            connection=self.crea_coneccion()
            print ('coneccion')
            connection.create_table('PERIODO_'+str(period)+':SEGUIMIENTO_'+nombre_curs,{'CMI_2022':{}})
            connection.close()

        except Exception as e:
            print('no se creo la tabla')
            print(e)
            connection.close()

    def crea_namespace(self,period,nombre_curs):
        try:
            connection=self.crea_coneccion()
            print ('coneccion')
            connection.create_namespace('PERIODO_'+str(period)+':SEGUIMIENTO_'+nombre_curs,{'CMI_2022':{}})
            connection.close()

        except Exception as e:
            print(e)
            connection.close()