
class SimulacionAfd:
    def __init__(self,afd,cadena):
        self.afd = afd.afn
        self.cadena = cadena+"#"
        self.estadofinal = afd.nodosfinales_afd
        self.iteraciones = 0
    
    def move(self,estado,c):
        for transicion in self.afd:
            if transicion[0] == estado and transicion[1] == c:
                return transicion[2]
        return None
    def sigCar(self):
        car = self.cadena[self.iteraciones]
        self.iteraciones += 1
        return car

    def simulacion_afd(self):
        s = 0
        c = self.sigCar()
        while(c != "#"):
            s = self.move(s,c)
            c = self.sigCar()

        if s in self.estadofinal:
            return True
        else:
            return False
            
        

