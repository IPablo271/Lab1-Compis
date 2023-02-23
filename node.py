
'''
Universidad del valle de Guatemala
Nombre: Pablo Gonzalez
Carnet: 20362
Proposito de clase: Esta clase tiene como proposito poder 
tener un objeto tipo nodo donde se alamcene informacion de cada nodo
esto se implemento asi debido a que en un futuro puede ser de ayuda 
tener data cargada en un objeto que represente un nodo en los diferentes diagramas.
'''
class Nodo:
    id_counter = 0 #Variavle para llevar un control de cuantos nodos se crean
    def __init__(self): #Constructor del nodo
        self.id = Nodo.id_counter
        Nodo.id_counter += 1
        



    
    

