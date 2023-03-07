from nododirecto import *
class Directa:
    def __init__(self,expression):
        self.expression = expression
        self.arbol = None
        self.lista_transiciones = []
    
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


            
            print("")
    


        

        




                
                