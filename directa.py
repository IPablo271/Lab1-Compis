from nododirecto import *
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

    
    def isOperator(self,caracter): #Metodo para verificar si es un operador
        return caracter == "*" or caracter =="." or caracter == "|" or caracter =="+" or caracter =="?"
    
    def print_posciciones_arol(self):
        for nodo in self.arbol.nodos:
            print(nodo.id)
    
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

    def print_followpos(self):
        print(self.followpos_arbol)
    
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

        print(self.tabla_final)

    def agregarcaracteres(self):
        for caracter in self.expression:
            if not self.isOperator(caracter):
                if caracter not in self.datos and caracter !="ε" and caracter !="#":
                    self.datos.append(caracter)
            else:
                pass

    def construccion_directo(self):
        self.construcion_tablafinal()
        estados_marcados = []
        estados_creados = {}
        lista_transiciones = []
        diccionario = {}
        self.agregarcaracteres()
        print(self.datos)


        




            
            

    

    
    


            
        
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
    


        

        




                
                