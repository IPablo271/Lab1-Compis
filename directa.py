from nododirecto import *
import graphviz
class Directa:
    def __init__(self,expression):
        self.expression = expression
        self.arbol = None
        self.nodos_letra = []
        self.id_letra = []
        self.followpos_arbol = []
        self.nodo_followpos = []
        self.lista_transiciones = []
        self.tabla_final = []
        self.datos = []
        self.estados_cojuntos = []
        self.afn = None
        self.afn_estados = None
        self.max = []

    
    def isOperator(self,caracter): #Metodo para verificar si es un operador
        return caracter == "*" or caracter =="." or caracter == "|" or caracter =="+" or caracter =="?"
    
    def print_posciciones_arol(self):
        for nodo in self.arbol.nodos:
            print(nodo.id)
            print(nodo.dato)
    
    def get_primer_nodo(self):
        nodo = self.arbol.nodos[-1]
        return nodo.firstPos
    
    
    def construccion_arbol(self):
        stack = []
        for caracter in self.expression:
            if not self.isOperator(caracter):
                nodotemp = Nododir(caracter)
                nodotemp.add_nodos(nodotemp)
                self.nullable(nodotemp)
                self.first_pos(nodotemp)
                self.last_pos(nodotemp)
                stack.append(nodotemp)
            else:
                if caracter == "." or caracter =="|":
                    nodo2 = stack.pop()
                    nodo1 = stack.pop()

                    if caracter ==".":
                        nodotemp = Nododir(caracter,izquierda=nodo1,derecha=nodo2)
                        for nodo in nodo1.nodos:
                            nodotemp.add_nodos(nodo)
                        for nodo in nodo2.nodos:
                            nodotemp.add_nodos(nodo)

                        nodotemp.add_nodos(nodotemp)
                        self.nullable(nodotemp)
                        self.first_pos(nodotemp)
                        self.last_pos(nodotemp)
                        self.followpos(nodotemp)
                        stack.append(nodotemp)
                    elif caracter == "|":
                        nodotemp = Nododir(caracter,izquierda=nodo1,derecha=nodo2)
                        for nodo in nodo1.nodos:
                            nodotemp.add_nodos(nodo)
                        for nodo in nodo2.nodos:
                            nodotemp.add_nodos(nodo)
                        nodotemp.add_nodos(nodotemp)
                        self.nullable(nodotemp)
                        self.first_pos(nodotemp)
                        self.last_pos(nodotemp)
                        stack.append(nodotemp)
                else:
                    if caracter == "*":
                        nodo1 = stack.pop()
                        nodotemp = Nododir(caracter,enmedio=nodo1)
                        for nodo in nodo1.nodos:
                            nodotemp.add_nodos(nodo)
                        nodotemp.add_nodos(nodotemp)
                        self.nullable(nodotemp)
                        self.first_pos(nodotemp)
                        self.last_pos(nodotemp)
                        self.followpos(nodotemp)
                        stack.append(nodotemp)
        
        self.arbol = stack[0]
        return stack[0]
    
    def nullable(self,nodo):
        if not self.isOperator(nodo.dato):
            if nodo.dato == 'ε':
                nodo.nullable = True
                return True
            else:
                nodo.nullable = False
                return False
        else:
            if nodo.dato == '|':
                nodo.nullable = nodo.izquierda.nullable or nodo.derecha.nullable
                return nodo.izquierda.nullable or nodo.derecha.nullable
            elif nodo.dato == '.':
                nodo.nullable = nodo.izquierda.nullable and nodo.derecha.nullable
                return nodo.izquierda.nullable and nodo.derecha.nullable
            elif nodo.dato == "*":
                nodo.nullable = True
                return True
    def first_pos(self,nodo):
        if not self.isOperator(nodo.dato):
            if nodo.dato == 'ε':
                pass
            else:
                nodo.firstPos.append(nodo.id)
        else:
            if nodo.dato == '|':
                lista1 = nodo.izquierda.firstPos
                lista2 = nodo.derecha.firstPos
                listan = lista1 + lista2
                listan.sort()
                nodo.firstPos = listan
            
            elif nodo.dato == '.':
                if self.nullable(nodo.izquierda):
                    lista1 = nodo.izquierda.firstPos
                    lista2 = nodo.derecha.firstPos
                    listan = lista1 + lista2
                    listan.sort()
                    nodo.firstPos = listan
                else:
                    nodo.firstPos = nodo.izquierda.firstPos

            elif nodo.dato == "*":
                nodo.firstPos = nodo.enmedio.firstPos
    def last_pos(self,nodo):
        if not self.isOperator(nodo.dato):
            if nodo.dato == 'ε':
                pass
            else:
                nodo.lastPos.append(nodo.id)
        else:
            if nodo.dato == '|':
                lista1 = nodo.izquierda.lastPos
                lista2 = nodo.derecha.lastPos
                listan = lista1 + lista2
                listan.sort()
                nodo.lastPos = listan
            
            elif nodo.dato == '.':
                if self.nullable(nodo.derecha):
                    lista1 = nodo.izquierda.lastPos
                    lista2 = nodo.derecha.lastPos
                    listan = lista1 + lista2
                    listan.sort()
                    nodo.lastPos = listan
                else:
                    nodo.lastPos = nodo.derecha.lastPos

            elif nodo.dato == "*":
                nodo.lastPos = nodo.enmedio.lastPos


        
    def followpos(self,nodo):
        if nodo.dato == '.':
            lista = []
            for dato in nodo.izquierda.lastPos:
                diccionario = {}
                nodoprimera = nodo.derecha.firstPos
                diccionario[dato] = nodoprimera
                lista.append(diccionario)
        
            nodo.followPos = lista
            self.followpos_arbol.append(lista)

        elif nodo.dato == '*':
            lista = []
            for dato in nodo.enmedio.lastPos:
                diccionario = {}
                nodoprimera = nodo.enmedio.firstPos
                diccionario[dato] = nodoprimera
                lista.append(diccionario)

            nodo.followPos = lista
            self.followpos_arbol.append(lista)

    def construccion_tabla(self):
        for nodo in self.arbol.nodos:
            diccionario = {}
            if not self.isOperator(nodo.dato):
                self.nodos_letra.append(nodo)
                diccionario[nodo.id] = nodo.dato
                self.id_letra.append(diccionario)

            else:
                pass
    
    def unify_values(self, key):
        result = {}
        for dict_list in self.followpos_arbol:
            for item in dict_list:
                for k, v in item.items():
                    if k == key:
                        result.setdefault(k, []).extend(v)
        if key not in result:
            result[key] = []

        return [{k: v} for k, v in result.items()]
    
    def construccion_nodofollowpos(self):
        for dict_item in self.id_letra:
            for key in dict_item.keys():
                lista = self.unify_values(key)
                self.nodo_followpos.append(lista[0])

    
    def construcion_tablafinal(self):
        self.construccion_tabla()
        self.construccion_nodofollowpos()
        keys = [clave for diccionario in self.id_letra for clave in diccionario.keys()]
        keys.sort()
        for i in range(len(self.nodo_followpos)):
            lista = []
            id_nodo = keys[i]
            dic = self.id_letra[i]
            dic2 = self.nodo_followpos[i]
            val1 = dic[id_nodo]
            val2 = dic2[id_nodo]
            lista.append(id_nodo)
            lista.append(val1)
            lista.append(val2)
            self.tabla_final.append(lista)


    def agregarcaracteres(self):
        for caracter in self.expression:
            if not self.isOperator(caracter):
                if caracter not in self.datos and caracter !="ε" and caracter !="#":
                    self.datos.append(caracter)
            else:
                pass

    def unirestados(self,estados,letra):
        estadosunion = []
        for estado in estados:
            for lista in self.tabla_final:
                if lista[0] == estado and lista[1] == letra:
                    estadosunion = estadosunion + lista[2]

        return estadosunion
    
    def buscar_llave(self,diccionario, valor_buscado):
        for llave, valor in diccionario.items():
            if valor == valor_buscado:
                return llave
        return None
    def encontrar_max(self):
        maximo = float('-inf')
        for sublista in self.afn:
            for numero in sublista:
                if isinstance(numero, int) and numero > maximo:
                    maximo = numero

        self.max.append(int(maximo))

        return maximo
    def encontrar_numeros(self):
        numeros = set()
        for sublista in self.afn:
            for elemento in sublista:
                if isinstance(elemento, int):
                    numeros.add(elemento)
        
        self.afn_estados = list(numeros)
        return list(numeros)

    def construccion_directo(self):
        self.construcion_tablafinal()
        estados_marcados = []
        estados_creados = 0
        lista_conneciones = []
        diccionario = {}
        self.agregarcaracteres()
        estado1 = self.get_primer_nodo()
        diccionario[estados_creados] = estado1

        for letra in self.datos:
            lista_temp = []
            estadoresult = self.unirestados(estado1,letra)
            lista_temp.append(estado1)
            lista_temp.append(letra)
            lista_temp.append(estadoresult)
            if len(estadoresult) > 0:
                lista_conneciones.append(lista_temp)

            if estadoresult not in self.estados_cojuntos:
                self.estados_cojuntos.append(estadoresult)
                estados_creados += 1
                diccionario[estados_creados] = estadoresult
        
        estados_marcados.append(estado1)

        for estado in self.estados_cojuntos:
            if estado not in estados_marcados:
                estados_marcados.append(estado)
                for letra in self.datos:
                    listatemp2 = []
                    estado_temp = self.unirestados(estado,letra)
                    listatemp2.append(estado)
                    listatemp2.append(letra)
                    listatemp2.append(estado_temp)
                    if len(estado_temp) > 0:
                        lista_conneciones.append(listatemp2)
                    if estado_temp not in self.estados_cojuntos:
                        self.estados_cojuntos.append(estado_temp)
                        estados_creados += 1
                        diccionario[estados_creados] = estado_temp

       
        listafinal = []
        for lista in lista_conneciones:
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

        self.encontrar_max()
        self.encontrar_numeros()
        print(self.afn_estados)
        print(self.max)
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
        g.render('afd_directo') 
        
    def print_arbol(self):
        a = self.arbol.nodos
        rev = list(reversed(a))
        for nodo in rev:
            print("Dato nodo: "+str(nodo.dato))

            if nodo.izquierda is not None:
                print("Izquierda del nodo: "+str(nodo.izquierda.dato))
            else:
                print("Izquierda del nodo: vacio")
            if nodo.derecha is not None:
                print("Deerecha del nodo: "+str(nodo.derecha.dato))
            else:
                print("Derecha del nodo: vacio")
            if nodo.enmedio is not None:
                print("Enmedio del nodo: "+str(nodo.enmedio.dato))
            else:
                print("Enmedio del nodo: vacio")
            if nodo.nullable is not None:
                print("El resultado de nullable para el nodo es: "+str(nodo.nullable))
            else:
                print("Nodo no nullable")
            if nodo.firstPos is not None:
                 print("El resultado de firstpos para el nodo es: "+str(nodo.firstPos))
            else:
                print("Nodo sin firstpos")
            if nodo.lastPos is not None:
                 print("El resultado de lastpos para el nodo es: "+str(nodo.lastPos))
            else:
                print("Nodo sin lastpos")
            if nodo.followPos is not None:
                 print("El resultado de followpos para el nodo es: "+str(nodo.followPos))
            else:
                print("Nodo sin followpos")


            
            print("")
    


        

        




                
                