
'''
Universidad del valle de Guatemala
Nombre: Pablo Gonzalez
Carnet: 20362
Proposito de clase: Esta clase tiene como proposito
implementar el algoritmo de Thompson para la construccion de 
un afn en donde se puede encontrar las diferentes reglas para sus 
operadores y asi mismo el metodo de construccion del afn
'''
from Transicion import *
from node import *
from Afn import *
class Thompson:
    def __init__(self,expresion): #Metdoo de constructor
        self.expresion = expresion #Expression en postfix del regex 
        self.listaNodos = []
        self.Dfa = None #Variable para alamcenar el anf final
    
    def simbolo(self,simbolo): #Funcion que devuelve un afn  1 por media de a -> 2
        nodo1 = Nodo() 
        nodo2 = Nodo() #Se crean los dos nodos a utlizar
        Transiciontemp = Transicion(nodo1,simbolo,nodo2) #Se crea la transicion del nodo1 al nodo 2 por medio de simbolo ingresado
        # nodo1.add_transicion(Transiciontemp)
        afntemp = AFN() #Se crea un afn temporal para almacenar la informacion
        afntemp.add_transicion(Transiciontemp) #Se agrega las transicones
        return afntemp #Se retorna el afn
    
    def ruleor(self,afn1, afn2):#Metodo para poder realizar la funcion or en donde se tiene como input dos afn y se devuelve un afn de la forma a|b
        afntemp = AFN() #Se crea el afn temporal que contendra el or de los dos afn
        nodo1 = Nodo()
        nodo2 = Nodo()#Se crean los dos nodos a utlizar
        Transiciontemp1 = Transicion(nodo1,"ε",afn1.transiciones[0].estadoinicial)
        Transiciontemp2 = Transicion(nodo1,"ε",afn2.transiciones[0].estadoinicial)
        #Se realizan dos transiciones una con nodo inicial del afn1 con epsilon y otra con el nodoinicial del afn2 las dos dirijidas al primer nodo creado
        # nodo1.add_transicion(Transiciontemp1)
        # nodo1.add_transicion(Transiciontemp2)


        afntemp.add_transicion(Transiciontemp1)
        afntemp.add_transicion(Transiciontemp2)
        #Se agren las dos transiciones temporales

        for transicion in afn1.transiciones:
            afntemp.add_transicion(transicion)
        for transicion in afn2.transiciones:
            afntemp.add_transicion(transicion)
        # Se agregan el restro de transiciones

        #Se realizan dos transiciones una con nodo final del afn1 con epsilon y otra con el nodo final del afn2 las dos dirijidas al segundo nodo creado

        nodotemp = afn1.transiciones[-1].estadofinal
        noodtemp2 = afn2.transiciones[-1].estadofinal

        Transiciontemp3 = Transicion(afn1.transiciones[-1].estadofinal,"ε",nodo2)
        Transiciontemp4 = Transicion(afn2.transiciones[-1].estadofinal,"ε",nodo2)

        afntemp.add_transicion(Transiciontemp3)
        afntemp.add_transicion(Transiciontemp4)
        #Se agren las dos transiciones temporales

        # nodotemp.add_transicion(Transiciontemp3)
        # noodtemp2.add_transicion(Transiciontemp4)

        return afntemp #Se retorna el afn nuevo
    
    def reglaKleen(self,afn1):#Metodo para poder realizar la funcion * en donde se tiene como input un afn y se devuelve un afn de la forma a*
        afntemp = AFN() #Se crea el afn temporal que contendra el or de los dos afn
        nodo1 = Nodo()
        nodo2 = Nodo() #Se crean los dos nodos a utlizar
        Transiciontemp1 = Transicion(nodo1,"ε",afn1.transiciones[0].estadoinicial)
        # nodo1.add_transicion(Transiciontemp1)
        #Se crea una transicion desde el nodo1 hacia el nodo inicial del afn por medio de epsilon
        afntemp.add_transicion(Transiciontemp1)
        #Se crea la transicion 

        for transicion in afn1.transiciones:
            afntemp.add_transicion(transicion)
        #Se agregan todas las transiciones del afn que se paso como paarmetro

        nodotemp1 = afn1.transiciones[-1].estadofinal

        Transiciontemp2 = Transicion(afn1.transiciones[-1].estadofinal,"ε",nodo2)
        #Se crea una transicion desde el nodo fianl del afn hacia el nodo 2 por medio de epsilon
        Transiciontemp3 = Transicion(afn1.transiciones[-1].estadofinal,"ε",afn1.transiciones[0].estadoinicial)
        #Se crea una transicion desde el nodo fianl del afn hacia el nodo inicial del afn por medio de epsilon
        Transiciontemp4 = Transicion(nodo1,"ε", nodo2)
        #Se crea una transicion desde el nodo1 del afn hacia el nodo2  del afn por medio de epsilon
        # nodotemp1.add_transicion(Transiciontemp2)
        # nodotemp1.add_transicion(Transiciontemp3)
        # nodo1.add_transicion(Transiciontemp4)

        afntemp.add_transicion(Transiciontemp2)
        afntemp.add_transicion(Transiciontemp3)
        afntemp.add_transicion(Transiciontemp4)
        #Se agregan las nuevas transicones al afn

        return afntemp #Se devuelve el afn con la regla
    
    def reglaconcat(self,afn1,afn2): #Metodo para poder realizar la funcion concatenacion en donde se tiene como input dos afn y se devuelve un afn de la forma a.b
        afntemp = AFN() #Se crea el afn temporal
        for transicion in afn1.transiciones: #Se agregan todas las transicones del primer afn
            afntemp.add_transicion(transicion)
        
        estadofinalAFN1 = afn1.transiciones[-1].estadofinal #Estado final del afn1
        estadInicialAFN2 = afn2.transiciones[0].estadoinicial #Estado inicial del afn2
        
        for transicion in afn2.transiciones: #Se recorre afd2
            if(transicion.estadoinicial == estadInicialAFN2): #Se verifica si el estado inciial de la transicion es igua al estado inciial del afn2
                transicion.estadoinicial = estadofinalAFN1 #Si es igual la transicion se vuelve el estado final del afn1 para hacer la concatenacion

        
        #Se agregan las transicones
        for transicion in afn2.transiciones:
            afntemp.add_transicion(transicion)
        
        lasttransicion = afntemp.transiciones[-1]
        nodoinicial = lasttransicion.estadoinicial
        # nodoinicial.add_transicion(lasttransicion)
        
        #Se retorna el afd
        return afntemp
    def rulecpositiva(self,afn1):#Metodo para poder realizar la funcion + en donde se tiene como input un afn y se devuelve un afn de la forma a+
        afntemp = AFN() #Se crea el afn temporal que contendra el or de los dos afn
        nodo1 = Nodo()
        nodo2 = Nodo() #Se crean los dos nodos a utlizar
        Transiciontemp1 = Transicion(nodo1,"ε",afn1.transiciones[0].estadoinicial)
        # nodo1.add_transicion(Transiciontemp1)


        #Se crea una transicion desde el nodo1 hacia el nodo inicial del afn por medio de epsilon
        afntemp.add_transicion(Transiciontemp1)
        #Se agrega la trannsiicon


        for transicion in afn1.transiciones:
            afntemp.add_transicion(transicion)
        #Se agregan todas las transiciones del afn que se paso como paarmetro
                

        nodotemp = afn1.transiciones[-1].estadofinal

        Transiciontemp3 = Transicion(afn1.transiciones[-1].estadofinal,"ε",afn1.transiciones[0].estadoinicial)
        #Se crea una transicion desde el nodo fianl del afn hacia el nodo inicial del afn por medio de epsilon
        Transiciontemp2 = Transicion(afn1.transiciones[-1].estadofinal,"ε",nodo2)
        #Se crea una transicion desde el nodo fianl del afn hacia el nodo 2 por medio de epsilon
        afntemp.add_transicion(Transiciontemp3)
        afntemp.add_transicion(Transiciontemp2)
        # nodotemp.add_transicion(Transiciontemp3)
        # nodotemp.add_transicion(Transiciontemp2)
        #Se agregan las nuevas transicones al afn

        return afntemp #Se retorna el afn 
    def reglaOrEpsilon(self,afn1): #Metodo para poder realizar la funcion or epsilon en donde se tiene como input un afn y se devuelve de forma a|ε
        afntemp = self.simbolo("ε") #Se crea un nodo epsilon
        return self.ruleor(afn1,afntemp) #Se retorna la regla or con el nuevo af con epsilon creado
    
    def isOperator(self,caracter): #Metodo para verificar si es un operador
        return caracter == "*" or caracter =="." or caracter == "|" or caracter =="+" or caracter =="?"

    def postfix_to_nfa(self): #Funcion que convierte el postfix de la experssion en un afn (Algoritmo de thompson)
        stack = [] #Se crea un stack para almacenar todos los afd del metodo de thompson
        for caracter in self.expresion: #For que recorre la expression
            if not self.isOperator(caracter): #Si no es un operador
                afn = self.simbolo(caracter) #Se ejecuta la regla de simbolo
                stack.append(afn) #Se almacena en el stack

            else: #Si es un operdador
                if caracter =="." or caracter =="|": #Si el operador es un operador que opera 2 afn
                    afn2 = stack.pop()
                    afn1 = stack.pop()
                    #Se extraen los de afn
                    if caracter == ".": #Si el caracter es. se ejecuta el concat
                        afn3 = self.reglaconcat(afn1,afn2)
                        stack.append(afn3)

                    elif caracter =="|": #Si el caracter es | se ejecuta el or
                        afn3 = self.ruleor(afn1,afn2)
                        stack.append(afn3)
                else: #Si el caracter solo necesita un afn
                    if caracter == "*": #Si el caracter es * se ejecuta el kleen
                        afntemp = stack.pop()
                        afntemp = self.reglaKleen(afntemp)
                        stack.append(afntemp)

                    elif caracter == "+": #Si el caracter es + se ejecuta la cerradura positiva
                        afntemp = stack.pop()
                        afntemp = self.rulecpositiva(afntemp)
                        stack.append(afntemp)
                    elif caracter == "?": #Si el caracter es ? se ejecuta el or epsilon
                        afntemp = stack.pop()
                        afntemp = self.reglaOrEpsilon(afntemp)
                        stack.append(afntemp)

        

        self.dfa = stack[0] #Se almacena el afn final en la variable de instacia
        return stack[0] #Se retorna el afn final 

