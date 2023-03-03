

class Subconjuntos:
    def __init__(self,afd):
        self.afd = afd
        self.nodos_afd = afd.nodes
        self.afn = None
        self.estados_conjuntos_num = []
        self.estados_conjuntos = []

    def print_nodos(self):
        for node in self.nodos_afd:
            print(node.id)
    
    def eclousere(self,estados):
        estados_temp = []
        estados_result = []
        estados_num = []
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
        
        for resultado in estados_result:
            estados_num.append(resultado.id)

        estados_num.sort()
        print(estados_num)
        self.estados_conjuntos_num.append(estados_num) 
        self.estados_conjuntos.append(estados_result)

        return estados_result
    
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
        print(estados_num)
        return estados_result
    

    
    

