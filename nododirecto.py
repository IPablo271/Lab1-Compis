
'''
Universidad del valle de Guatemala
Nombre: Pablo Gonzalez
Carnet: 20362
Proposito de clase: Esta clase tiene como proposito poder 
tener un objeto tipo nodo donde se alamcene informacion de cada nodo
esto se implemento asi debido a que en un futuro puede ser de ayuda 
tener data cargada en un objeto que represente un nodo en los diferentes diagramas.
'''
class Nododir:
    id_counter = 0 #Variavle para llevar un control de cuantos nodos se crean
    def __init__(self,dato,izquierda = None , enmedio = None, derecha = None): #Constructor del nodo
        self.id = Nododir.id_counter
        Nododir.id_counter += 1
        self.dato = dato
        self.izquierda = izquierda
        self.enmedio = enmedio
        self.derecha = derecha
        self.nodos = []
        self.nullable = None
        self.firstPos = []
        self.lastPos = []
        self.followPos = []
    
    def add_nodos(self,nodo):
        self.nodos.append(nodo)
    
    

        
              

        
    
    


        



    
    

