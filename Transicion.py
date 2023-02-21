from node import *
class Transicion:
    def __init__(self,nodo1,dato,nodo2):
        self.estadoinicial = nodo1
        self.estadofinal = nodo2
        self.dato = dato

    def __str__(self):
        print("estado inicial: " +str(self.izquierda.id) +" estado final "+str(self.derecha) +" Dato: "+str(self.dato))

