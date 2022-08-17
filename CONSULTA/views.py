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
            
            table_i= connection.table('PERIODO_'+str(periodo)+':SEGUIMIENTO_'+curso)
        
        
            filter_text="SingleColumnValueFilter('CMI_2022','renipress_adscripcion',=, 'binary:"+ipress+"',false,true)"
            print(filter_text)
            for key, data in table_i.scan(filter=filter_text):
          
                
                activida=[]
                data_fil={}
                data_fil=filter(lambda ac:self.util(ac,id_indicador),data.items())
                for key1,data1 in data_fil:
                    
                    indices=key1.decode('utf-8').split('$')
                    indicador=indices[1]
                    campo= indices[2]
                    existe=False
                    
                    indice_encontrar=1000
                    
                  
                    for i in range(0, len(activida)):
                       
                      

                        if activida[i]["indicador"]== indices[1]:
                            existe=True 
                            indice_encontrar=i
                            activida[indice_encontrar][indices[2]]=data1.decode('utf-8')                    
                           
                        else:
                            existe=False
                    
                    if existe==False:
                        activida.append({"indicador":indices[1]})
                        activida[len(activida)-1][indices[2]]=data1.decode('utf-8')
                        activida[len(activida)-1]["padre"]=id_indicador
                            
                  
                        
                       

                if len(activida)!=0:

                    lisg.append({'numero_documento':key.decode('utf-8'),'actividades':activida})
         
            connection.close()
            
        except Exception as e:
            print (e)
            print ('error de coneccion')
            
        


            '''
                lisg[key.decode('utf-8')]=json.dumps(data)
                print('============================================================')
                print(type(data))
                
                print('============================================================')
            
            
            '''


        return JsonResponse(lisg,safe=False)
    
    def Crea_coneccion(self):
        try:
            print(os.environ.get('SERVER_HBASE'))
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
        if dos=='Apellido_Paterno_Paciente':
            return True
        if dos=='Apellido_Materno_Paciente':
            return True
        if dos=='Nombres_Paciente':
            return True
        
        
        return indi==dos