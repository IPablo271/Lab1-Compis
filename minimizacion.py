
class Minimizacion:
    def __init__(self,afd):
        self.afd = afd.afn
        self.nodos_f = afd.nodosfinales_afd
        self.nodos_s = afd.nodos_no_finales_afd
        self.afd_minimizado = None
        self.primera_particion = []
        self.particion = []
        self.datos = []

    def unir_listas(self):
        self.primera_particion.append(self.nodos_f)
        self.primera_particion.append(self.nodos_s)
    def agregar_caracteres(self):
        caracteres_agregados = []
        for sublista in self.afd:
            caracter = sublista[1]
            if caracter not in caracteres_agregados:
                caracteres_agregados.append(caracter)
        
        self.datos = caracteres_agregados
        return caracteres_agregados
    def ordenar_sublistas(self,lista):
        nueva_lista = []
        for sublista in lista:
            nueva_sublista = sorted(sublista)
            nueva_lista.append(nueva_sublista)
        return nueva_lista
    
    
    

    


    def minimizacion_afd(self):
        self.unir_listas()
        self.agregar_caracteres()
        self.primera_particion = self.ordenar_sublistas(self.primera_particion)

        

        
