from pickle import TRUE
from django.shortcuts import render
from http.client import HTTPResponse
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
# Create your views here.
import happybase as hb
import json
import os

# Create your views here.
class consulta(View):
    separador='$'
    def get(self, request,agnio,mes,ipress,id_indicador,curso):
        
        periodo=str(int(agnio)*100+int(mes))
        lisg=[]
        try:
            connection=self.Crea_coneccion()
            
            print('PERIODO_'+str(periodo)+':SEGUIMIENTO_'+curso)
            
            table_i= connection.table('PERIODO_'+str(periodo)+':SEGUIMIENTO_'+curso)
        
            filter_text="SingleColumnValueFilter('CMI_2022','renipress_adscripcion',=, 'binary:"+ipress+"',false,false)"
            print(filter_text)
            for key, data in table_i.scan(filter=filter_text,limit=20):
                persona={'numero_docuemnto':key.decode('utf-8')}
          
                
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
            
            return con
        except Exception as e:
            print('error de coneccion')
            print (e)
            con.close()
    def util(self,uno,dos):
     
        uno[0].decode('utf-8').split('$')
        indi=uno[0].decode('utf-8').split('$')[0].split(':')[1]
  
        
    
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