class Corazon:
    id_counter = 0 #Variavle para llevar un control de cuantos nodos se crean
    def __init__(self): #Constructor del nodo
        self.id = Corazon.id_counter
        Corazon.id_counter += 1
        self.corazon = {}
        self.cerradura = {}
        self.irA = []
        self.transiciones = []
    def __str__(self):
        estado_str = f"Estado: {self.id}\n"
        corazon_str = f"Corazon: {self.corazon}\n"
        productions_str = "Producciones:\n"

        for key, value in self.cerradura.items():
            productions_str += f"{key}: {', '.join(value)}\n"
        
        transiciones_str = "Transiciones:\n"
        for transicion in self.transiciones:
            transiciones_str += str(transicion) + "\n"
        
        return f"{estado_str}{corazon_str}{productions_str}{transiciones_str}"


        
    def add_irA(self,irAtrans):
        self.irA.append(irAtrans)
        
    def add_cerradura(self,cerradura):
        self.cerradura.append(cerradura)
