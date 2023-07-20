import graphviz
class Minimizacion:
    def __init__(self,afd):
        self.afd = afd.afn
        self.nodos_f = afd.nodosfinales_afd
        self.nodos_s = afd.nodos_no_finales_afd
        self.afd_minimizado = None
        self.primera_particion = []
        self.particion = []
        self.particionnueva = []
        self.datos = []
        self.diccionariofinal = None

    def unir_listas(self):
        self.primera_particion.append(self.nodos_f)
        self.primera_particion.append(self.nodos_s)
    def agregar_caracteres(self):
        caracteres_agregados = []
        for sublista in self.afd:
            caracter = sublista[1]
            if caracter not in caracteres_agregados:
                caracteres_agregados.append(caracter)
        
        self.datos = caracteres_agregados
        return caracteres_agregados
    def ordenar_sublistas(self,lista):
        nueva_lista = []
        for sublista in lista:
            nueva_sublista = sorted(sublista)
            nueva_lista.append(nueva_sublista)
        return nueva_lista
    
    def buscar_grupo(self,numero, diccionario):
        for key, value in diccionario.items():
            if numero in value:
                return key
        return []
        

    def buscar_valor(self,num, letra):
        for sublista in self.afd:
            if sublista[0] == num and sublista[1] == letra:
                return sublista[2]
        return []
    def buscar_clave(self,diccionario, valor_buscado):
        for clave, valor in diccionario.items():
            if valor == valor_buscado:
                return clave
        else:
            return None
    
    
    def dividir_subgrupos(self,grupo):
      
        # print(grupo)
        estado_creado = 0
        diccionario = {}
        for lista in grupo:
            diccionario[estado_creado] = lista
            estado_creado +=1
        
        # print(diccionario)
        listafinal = []
        lista_tabla = []
        for lista in grupo:
            if len(lista) <= 1:
                listafinal.append(lista)
            else:
                for nodo in lista:
                    listanodo = []
                    for letra in self.datos:
                        listatemp = []
                        valor = self.buscar_valor(nodo,letra)
                        grupo = self.buscar_grupo(valor,diccionario)
                        listatemp.append(nodo)
                        listatemp.append(letra)
                        listatemp.append(grupo)
                        listanodo.append(listatemp)
                    lista_tabla.append(listanodo)
                
                listatuplas = []
                for sublista in lista_tabla:
                    listatemp = []
                    for lista in sublista:
                        listatemp.append(lista[2])
                    if listatemp not in listatuplas:
                        listatuplas.append(listatemp)
                
                diccionarioidentificaicon = {}
                numtuplas = 0
                for listat in listatuplas:
                    diccionarioidentificaicon[numtuplas] = listat
                    numtuplas +=1
                
                diccionario_final = {}
                for sublista in lista_tabla:
                    listatempf = []
                    datotemp = None
                    for lista in sublista:
                        datotemp = lista[0]
                        dato = lista[2]
                        listatempf.append(dato)

                    # print("Lista que se esta buscando: "+str(listatempf))
                    id_n = self.buscar_clave(diccionarioidentificaicon,listatempf)
                    diccionario_final[datotemp] =id_n
                
                listas_por_valor = []
                valores = set(diccionario_final.values())  # obtenemos todos los valores distintos del diccionario
                for valor in valores:
                    lista_keys = [key for key in diccionario_final.keys() if diccionario_final[key] == valor]
                    listas_por_valor.append(lista_keys)

                for lista in listas_por_valor:
                    listafinal.append(lista)
                
                
        # print("Lista tabla: "+str(lista_tabla))
        # print("Lista tuplas: "+str(listatuplas))
        # print("Diccionario identificacion: "+str(diccionarioidentificaicon))
        # print("Diccionario final: "+str(diccionario_final))
        # print("Lista final de los subgrupos: "+str(listas_por_valor))
        # print("Lista final de estados: "+str(listafinal))
        sin_repetidos = list(set(tuple(i) for i in listafinal))
        sin_repetidos = [list(i) for i in sin_repetidos]

        return sin_repetidos
    
    def devolver_transicion(self,lista):
        representante = lista[0]
    
    def comparar_listas(self,lista1, lista2):
        if len(lista1) != len(lista2):
            return False
        for elemento in lista1:
            if elemento not in lista2:
                return False
        return True

    
    def obtener_transicion(self,num, letra):
        for sublista in self.afd:
            if sublista[0] == num and sublista[1] == letra:
                dato = sublista[2]
                return dato
                
    
    def get_grupo(self, numero):
        for key, lista in self.diccionariofinal.items():
            if numero in lista:
                return key
        return []

    def obtener_posicion(self,numero, letra):
        for sublista in self.afd:
            if sublista[0] == numero and sublista[1] == letra:
                return sublista[2]
        return None
    
    def prueba_minimizacion(self,):
        self.unir_listas()
        self.agregar_caracteres()
        self.particionnueva = self.ordenar_sublistas(self.primera_particion)
        particion = self.dividir_subgrupos(self.particionnueva)
        print(particion)
        particion2 = self.dividir_subgrupos(particion)
        print(particion2)
        particion3 = self.dividir_subgrupos(particion2)
        print(particion3)

    
    def minimizacion_afd(self):
        self.unir_listas()
        self.agregar_caracteres()
        self.particionnueva = self.ordenar_sublistas(self.primera_particion)

       
        
        while  self.comparar_listas(self.particionnueva,self.particion) != True:
            self.particion = self.particionnueva
            self.particionnueva = self.dividir_subgrupos(self.particionnueva)

            

        for i in range(len(self.particionnueva)):
            self.particionnueva[i] = sorted(self.particionnueva[i])
        
        self.particionnueva = [sublista for sublista in self.particionnueva if sublista]
        

        
        self.particionnueva = sorted(self.particionnueva,key=lambda x:x[0])
        dic = {}
        numgroup = 0
        for lista in self.particionnueva:
            dic[numgroup] = lista
            numgroup += 1
        
        self.diccionariofinal = dic
        transiciones_finales = []
        
        for lista in self.particionnueva:
            for dato in self.datos:
                listatemporal = []
                datoinicial = lista[0]
                datotrans = self.obtener_posicion(datoinicial,dato)
                datoinicial = self.get_grupo(datoinicial)
                datotrans = self.get_grupo(datotrans)

                if type(datotrans) == int:
                    listatemporal.append(datoinicial)
                    listatemporal.append(dato)
                    listatemporal.append(datotrans)
                    transiciones_finales.append(listatemporal)

        self.afd_minimizado = transiciones_finales
        return transiciones_finales

       
                
                

    
    def draw_afd_minimizado(self): #Metodo para dibujar el digrafo con la liberia graphviz
        g = graphviz.Digraph(graph_attr={'rankdir': 'LR'})  
        nodes = []
        for edge in self.afd_minimizado:
            src = edge[0]
            dest = edge[2]
            label = edge[1]
            if src not in nodes:
                g.node(str(src))
                nodes.append(src)
            if dest not in nodes:
                g.node(str(dest))
                nodes.append(dest)
            g.edge(str(src), str(dest), label=label, dir='forward', arrowhead='vee') 
        g.format = 'png'
        g.render('afdMinimizado')
    
       

        
        




        

        
