from pickle import TRUE
from django.shortcuts import render
from http.client import HTTPResponse
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import happybase as hb
import json
import os

# Create your views here.
class consulta(View):
    separador='$'
    @csrf_exempt
    def post(self, request,agnio,mes,id_indicador,curso):        
        
        body_unicode = request.body.decode('utf-8')
   
        dta=json.loads(body_unicode)
     
        cadena_filtro="(QualifierFilter(=, 'regexstring:renipress_adscripcion') OR QualifierFilter(=, 'regexstring:ipress_adscripcion') OR QualifierFilter(=, 'regexstring:"+id_indicador+"$*')) AND ("
        
        for ip in dta['IPRESS']:
         
            if cadena_filtro=="(QualifierFilter(=, 'regexstring:renipress_adscripcion') OR QualifierFilter(=, 'regexstring:ipress_adscripcion') OR QualifierFilter(=, 'regexstring:"+id_indicador+"$*')) AND (":
                cadena_filtro=cadena_filtro+" SingleColumnValueFilter('CMI_2022','renipress_adscripcion',=, 'binary:"+ip+"',false,false)"
            else:
                cadena_filtro=cadena_filtro+" OR SingleColumnValueFilter('CMI_2022','renipress_adscripcion',=, 'binary:"+ip+"',false,false)"
        
        
        cadena_filtro=cadena_filtro+" )"
           
        periodo=str(int(agnio)*100+int(mes))
        lisg=[]
        try:
            connection=self.Crea_coneccion()
            
            print('PERIODO_'+str(periodo)+':SEGUIMIENTO_'+curso)
            
            table_i= connection.table('PERIODO_'+str(periodo)+':SEGUIMIENTO_'+curso)
        
            print(cadena_filtro)
         
            for key, data in table_i.scan(filter=cadena_filtro):
                persona={'numero_documento':key.decode('utf-8')}          
                
                activida=[]
                data_fil={}
             
                data_fil=filter(lambda ac:self.util(ac,id_indicador),data.items())
                for key1,data1 in data_fil:
                    
                    indices=key1.decode('utf-8').split('$')
                    es_encabesado=False
                    valor_encabesado=''
                    encabesado=''
                    
                    indicador=10000000
                    campo='marte'
                    if len(indices)>1:
                        indicador=indices[1]
                        campo= indices[2]
                    else:
                        encabesado=key1.decode('utf-8').split(':')[1]
                        valor_encabesado=data1.decode('utf-8')
                        es_encabesado=True
                        
                        
                    
                    existe=False
                    
                    indice_encontrar=1000
                    
                  
                    for i in range(0, len(activida)):           
                        
                        
                                      

                        if activida[i]["indicador"]== indicador :
                            existe=True 
                            indice_encontrar=i
                            if es_encabesado==False:
                                activida[indice_encontrar][campo]=data1.decode('utf-8')                    
                           
                        else:
                            existe=False
                    
                    if existe==False :
                        if campo!='marte':
                            activida.append({"indicador":indicador})
                        
                            activida[len(activida)-1][campo]=data1.decode('utf-8')
                            activida[len(activida)-1]["padre"]=id_indicador
                        if campo!='marte':
                            activida[len(activida)-1][encabesado]=valor_encabesado
                    
                   
                   
                    if es_encabesado==True:
                        
                        persona[encabesado]=valor_encabesado
                       
                        
                            
                  
                        
                       

                if len(activida)!=0:
                    persona['actividades']=activida

                    lisg.append(persona)
         
            connection.close()
            
        except Exception as e:
            print (e)
            print ('error de coneccion')
            
        




        return JsonResponse(lisg,safe=False)
    
    def Crea_coneccion(self):
        try:
            
            con=  hb.Connection(os.environ.get('SERVER_HBASE'),port=int(os.environ.get('PORT_HBASE')) )
            print('conneccion exitosa')
            
            return con
        except Exception as e:
            print('error de coneccion 132')
            print (e)
            con.close()
            
    def util(self,uno,dos):
     
        uno[0].decode('utf-8').split('$')
        indi=uno[0].decode('utf-8').split('$')[0].split(':')[1]
  
        return True
    
        if indi==dos: 
            return True
        if uno[0].decode('utf-8').split(':')[1]=='Apellido_Paterno_Paciente':
        
            
            return True
        if uno[0].decode('utf-8').split(':')[1]=='Apellido_Materno_Paciente':
   
            return True
        if uno[0].decode('utf-8').split(':')[1]=='Nombres_Paciente':
            return True
        if uno[0].decode('utf-8').split(':')[1]=='renipress_adscripcion':
            return True
        if uno[0].decode('utf-8').split(':')[1]=='ipress_adscripcion':
            return True
        
        
        return indi==dos