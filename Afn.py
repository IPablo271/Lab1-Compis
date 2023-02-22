import graphviz
class AFN:
    def __init__(self):
        self.transiciones = []
        self.transicionesNum = []
    

    def add_transicion(self,transicion):
        self.transiciones.append(transicion)
    
    def printAfn(self):
        for transicion in self.transiciones:
            print(str(transicion.estadoinicial.id) +" "+str(transicion.dato) +" "+str(transicion.estadofinal.id))

    def transicionesToNum(self):
        for transicion in self.transiciones:
            lista = []
            nodo1 = transicion.estadoinicial.id
            nodo2 = transicion.estadofinal.id
            dato = transicion.dato
            lista.append(nodo1)
            lista.append(dato)
            lista.append(nodo2)
            self.transicionesNum.append(lista)
    def draw_graph(self):
        g = graphviz.Graph()
        nodes = []
        for edge in self.transicionesNum:
            src = edge[0]
            dest = edge[2]
            label = edge[1]
            if src not in nodes:
                g.node(str(src))
                nodes.append(src)
            if dest not in nodes:
                g.node(str(dest))
                nodes.append(dest)
            g.edge(str(src), str(dest), label=label)
        g.format = 'png'
        g.render('graph')
