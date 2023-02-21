class AFN:
    def __init__(self):
        self.transiciones = []
    

    def add_transicion(self,transicion):
        self.transiciones.append(transicion)
    
    def printAfn(self):
        for transicion in self.transiciones:
            print(str(transicion.estadoinicial.id) +" "+str(transicion.dato) +" "+str(transicion.estadofinal.id))