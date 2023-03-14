class SimulacionAfn:
    def __init__(self,afn,cadena):
        self.afn = afn.transicionesNum
        self.nodos_afd = afn.nodes
        self.cadena = cadena+"#"
        self.datos = []
        self.estadofinal = afn.nodosfinales_afn
        self.iteraciones = 0

    def agregar_caracteres(self):
        for lista in self.afn:
            if lista[1] not in self.datos:
                self.datos.append(lista[1])
            else:
                pass
    
    def eclousere(self,estados):
        estados_temp = []
        estados_result = []
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

        return estados_result
    def estados_nodos_to_num(self,estados_result):
        estados_num = []
        for resultado in estados_result:
            estados_num.append(resultado.id)
        estados_num.sort()
        return estados_num 
    

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
        return estados_result
    


    
    def sigCar(self):
        car = self.cadena[self.iteraciones]
        self.iteraciones += 1
        return car

    def simulacion_afn(self):
        lista = []
        lista.append(self.nodos_afd[0])
        estado = self.eclousere(lista)
        c = self.sigCar()

        while (c != "#"):
            estadomove = self.mover(estado,c)
            estado = self.eclousere(estadomove)
            c = self.sigCar()
        
        estado_num = self.estados_nodos_to_num(estado)
        interseccion = list(set(estado_num) & set(self.estadofinal))

        if len(interseccion) >0:
            return True
        else:
            return False


        
            