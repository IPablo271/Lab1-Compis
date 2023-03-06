import graphviz
class Subconjuntos:
    def __init__(self,afd):
        self.afd = afd
        self.nodos_afd = afd.nodes
        self.afn = None
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
                    # print("Estado resultado del mov: "+str(self.estados_nodos_to_num(estado_temp)))
                    # print("Estado donde va: "+str(self.estados_nodos_to_num(estado)))
                    # print("Letra del estado: "+str(letra))
                    # print("Estado resultante: "+str(self.estados_nodos_to_num(estado_temp_result)))
                    # print("  ")

                    lista_temp2.append(self.estados_nodos_to_num(estado))
                    lista_temp2.append(letra)
                    lista_temp2.append(self.estados_nodos_to_num(estado_temp_result))
                    lista_conecciones.append(lista_temp2)
                    if estado_temp_result not in self.estados_conjuntos:
                        self.estados_conjuntos.append(estado_temp_result)
                        estados_creados += 1
                        estadi_num_temp = self.estados_nodos_to_num(estado_temp_result)
                        diccionario[estados_creados] = estadi_num_temp
        
        listafinal = []
        for lista in lista_conecciones:
            lista_temp_f = []
            llave = self.buscar_llave(diccionario,lista[0])
            dato = lista[1]
            llave2 = self.buscar_llave(diccionario,lista[2])
            lista_temp_f.append(llave)
            lista_temp_f.append(dato)
            lista_temp_f.append(llave2)
            listafinal.append(lista_temp_f)
        

        unique_listaf = []

        for lista in listafinal:
            if lista not in unique_listaf:
                unique_listaf.append(lista)
        
        self.afn = unique_listaf

        return listafinal
    
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


            


        
                        
        
    

         





        
        

                
    

    
    

