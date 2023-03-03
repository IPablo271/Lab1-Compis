
'''
Universidad del valle de Guatemala
Nombre: Pablo Gonzalez
Carnet: 20362
Proposito de clase: Esta clase tiene como proposito pdoer crear
objetos de tipo transicion entre dos nodos alamcenado el nodo incial
y el nodo final, conjuntamente al dato que uno dichas Transiciones
'''

from node import *
class Transicion:
    def __init__(self,nodo1,dato,nodo2): #Constructo de la clase Transicion
        self.estadoinicial = nodo1
        self.estadofinal = nodo2
        self.dato = dato

    def print_transicion(self): #Metodo para imprimir ela transicion
        print("estado inicial: " +str(self.estadoinicial.id) +" estado final "+str(self.estadofinal.id) +" Dato: "+str(self.dato))

