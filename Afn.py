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
    def draw_graph(self): #Metodo para dibujar el digrafo con la liberia graphviz
        g = graphviz.Digraph()  
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
        g.render('graph')

