'''
Universidad del valle de Guatemala
Nombre: Pablo Gonzalez
Carnet: 20362
Proposito de clase: Esta clase tiene como propoisito el poder
almacenar toda la informacion que conlleva un afn, como sus 
diferentes transiciones y dibujarse a si mismo en un formato de
png
'''
import graphviz
class AFN:
    def __init__(self): #Constructor de la clase
        self.transiciones = []
        self.nodes = []
        self.transicionesNum = []
    

    def add_transicion(self,transicion): #Se agrega una transicion al grafo
        self.transiciones.append(transicion)
    
    def printAfn(self): #Se imprime las transiciones del afn
        for transicion in self.transiciones:
            print(str(transicion.estadoinicial.id) +" "+str(transicion.dato) +" "+str(transicion.estadofinal.id))

    def transicionesToNum(self): #Metodo para guardar en una lista de lista las transiciones como int y no como objetos de tipo transicion
        for transicion in self.transiciones:
            lista = []
            nodo1 = transicion.estadoinicial.id
            nodo2 = transicion.estadofinal.id
            dato = transicion.dato
            lista.append(nodo1)
            lista.append(dato)
            lista.append(nodo2)
            self.transicionesNum.append(lista)
    def add_nodes(self):
        for transicion in self.transiciones:
            nodo1 = transicion.estadoinicial
            nodo2 = transicion.estadofinal
            if nodo1 not in self.nodes:
                self.nodes.append(nodo1)
            if nodo2 not in self.nodes:
                self.nodes.append(nodo2)
    def add_nodes_transiciones(self):
        for transicion in self.transiciones:
            nodo1 = transicion.estadoinicial
            nodo1.add_transicion(transicion)
    
    def print_movimientos_nodo(self):
        for nodo in self.nodes:
            print("Nodo: "+str(nodo.id))
            for transicion in nodo.transiciones:
                print(str(transicion.estadoinicial.id) +" "+str(transicion.dato) +" "+str(transicion.estadofinal.id))

        
    def draw_graph(self): #Metodo para dibujar el digrafo con la liberia graphviz
        g = graphviz.Digraph(graph_attr={'rankdir': 'LR'})  
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
            g.edge(str(src), str(dest), label=label, dir='forward', arrowhead='vee') 
        g.format = 'png'
        g.render('afn')
    



