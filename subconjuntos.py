import graphviz
class Subconjuntos:
    def __init__(self,afd):
        self.afd = afd
        self.nodos_afd = afd.nodes
        self.afn = None
        self.nodof_afd = None
        self.nodosfinales_afd = []
        self.nodos_no_finales_afd = []
        self.afd.estados = []
        self.estados_conjuntos_num = []
        self.estados_conjuntos = []
        self.datos = []

    def print_nodos(self):
        for node in self.nodos_afd:
            print(node.id)
    def agregar_caracteres(self):
        for transicion in self.afd.transiciones:
            if transicion.dato not in self.datos and transicion.dato != "ε":
                self.datos.append(transicion.dato)
            else:
                pass
    def encontrar_max(self):
        nodos = []
        for nodo in self.nodos_afd:
            nodos.append(nodo.id)
        maximo = max(nodos)
        self.nodof_afd = maximo
        return maximo
    def seprar_nodos(self,diccionario):
        lista_keys = []
        lista_nodos_n = []
        for key, lista_valores in diccionario.items():
            if self.nodof_afd in lista_valores:
                lista_keys.append(key)
            else:
                lista_nodos_n.append(key)
        


        self.nodos_no_finales_afd = lista_nodos_n
        self.nodosfinales_afd = lista_keys

        return lista_keys
    def find_estado_error(self,d):
        for k, v in d.items():
            if not v:  # si la lista es vacía
                return k
        return None 

    
    
    def eclousere(self,estados):
        estados_temp = []
        estados_result = []
        for estado in estados:
            estados_result.append(estado)
            estados_temp.append(estado)
        
         
        for nodo in estados_temp:
            for transicion in nodo.transiciones:
                if transicion.dato == "ε":
                    estados_result.append(transicion.estadofinal)
                    estados_temp.append(transicion.estadofinal)
                else:
                    pass

        return estados_result
    
    def estados_nodos_to_num(self,estados_result):
        estados_num = []
        for resultado in estados_result:
            estados_num.append(resultado.id)
        estados_num.sort()
        self.estados_conjuntos_num.append(estados_num)
        return estados_num 

    
    def mover(self,estados,char):
        estados_result = []
        estados_num = []

         
        for nodo in estados:
            for transicion in nodo.transiciones:
                if transicion.dato == char:
                    estados_result.append(transicion.estadofinal)
                else:
                    pass
        
        for resultado in estados_result:
            estados_num.append(resultado.id)

        estados_num.sort()
        return estados_result
    
    def buscar_llave(self,diccionario, valor_buscado):
        for llave, valor in diccionario.items():
            if valor == valor_buscado:
                return llave
        return None

    def construccion_subconjuntos(self):
        self.encontrar_max()
        estados_marcados = []
        diccionario = {}
        lista_conecciones = []
        estados_creados = 0
        self.agregar_caracteres()


        lista = []
        lista.append(self.nodos_afd[0])

        estado1 = self.eclousere(lista)

        estado_num =self.estados_nodos_to_num(estado1)

        self.estados_conjuntos.append(estado1)

        diccionario[estados_creados] = estado_num

        for letra in self.datos:
            lista_temp =[]
            estado = self.mover(estado1,letra)
            estadoresult = self.eclousere(estado)
            lista_temp.append(self.estados_nodos_to_num(estado1))
            lista_temp.append(letra)
            lista_temp.append(self.estados_nodos_to_num(estadoresult))
            lista_conecciones.append(lista_temp)

            if estadoresult not in self.estados_conjuntos:
                self.estados_conjuntos.append(estadoresult)
                estados_creados += 1
                estadi_num_temp = self.estados_nodos_to_num(estadoresult)
                diccionario[estados_creados] = estadi_num_temp
                

                
        
        estados_marcados.append(estado1)
       
        
        for estado in self.estados_conjuntos:
            
            if estado not in estados_marcados:
                estados_marcados.append(estado)
                for letra in self.datos:
                    lista_temp2 = []
                    estado_temp = self.mover(estado,letra)
                   
                    estado_temp_result = self.eclousere(estado_temp)
                   

                    lista_temp2.append(self.estados_nodos_to_num(estado))
                    lista_temp2.append(letra)
                    lista_temp2.append(self.estados_nodos_to_num(estado_temp_result))
                    lista_conecciones.append(lista_temp2)
                    if estado_temp_result not in self.estados_conjuntos:
                        self.estados_conjuntos.append(estado_temp_result)
                        estados_creados += 1
                        estadi_num_temp = self.estados_nodos_to_num(estado_temp_result)
                        diccionario[estados_creados] = estadi_num_temp
        
        

        self.seprar_nodos(diccionario)
        estado_error = self.find_estado_error(diccionario)
        if estado_error != None:
            self.nodos_no_finales_afd.remove(estado_error)
        

        listafinal = []
        for lista in lista_conecciones:
            lista_temp_f = []
            llave = self.buscar_llave(diccionario,lista[0])
            dato = lista[1]
            llave2 = self.buscar_llave(diccionario,lista[2])

            if len(lista[0]) > 0 and len(lista[2]) >0:
                lista_temp_f.append(llave)
                lista_temp_f.append(dato)
                lista_temp_f.append(llave2)
                listafinal.append(lista_temp_f)
            

        unique_listaf = []

        for lista in listafinal:
            if lista not in unique_listaf:
                unique_listaf.append(lista)
        
        self.afn = unique_listaf

        return unique_listaf
    
    def draw_afd(self): #Metodo para dibujar el digrafo con la liberia graphviz
        g = graphviz.Digraph(graph_attr={'rankdir': 'LR'})  
        nodes = []
        for edge in self.afn:
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
        g.render('afd')


            


        
                        
        
    

         





        
        

                
    

    
    

