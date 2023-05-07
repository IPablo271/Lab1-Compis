class Yapar:
    def __init__(self, archivo):
        self.producciones = {}
        self.tokens = []
        self.producciones_unidas = {}
        self.no_terminales = []
        self.terminales = []
        with open(archivo, 'r') as f:
            produccion_actual = ''
            for linea in f:
                linea = linea.strip()
                if linea.startswith('/*') and linea.endswith('*/'):
                    continue
                if linea.startswith('%token'):
                    self.tokens.extend(linea.split()[1:])

                if linea.endswith(':'):
                    produccion_actual = linea[:-1]
                    self.producciones[produccion_actual] = []
                elif produccion_actual != '':
                    self.producciones[produccion_actual].append(linea)
                if linea.endswith(';'):
                    produccion_actual = ''
            for key, value in self.producciones.items():
                produccion_unida = ' '.join(value[:-1])
                self.producciones_unidas[key] = produccion_unida
    
    def compile(self):
        self.con_terminales()


    def con_terminales(self):
        for value in self.producciones_unidas.values():
            palabras = value.split()
            for palabra in palabras:
                if palabra.islower():
                    if palabra not in self.no_terminales:
                        self.no_terminales.append(palabra)
                else:
                    if palabra not in self.terminales and palabra != "|":
                        self.terminales.append(palabra)

        print(self.no_terminales)
        print(self.terminales)
    def get_tokens(self):
        return self.tokens

    def get_producciones(self):
        return self.producciones_unidas


yapar = Yapar("yapa.yalp")
print(yapar.get_tokens())
print(yapar.get_producciones())
yapar.compile()