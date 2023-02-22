from Transicion import *
from node import *
from Afn import *
class Thompson:
    def __init__(self,expresion):
        self.expresion = expresion
        self.Dfa = None
    
    def simbolo(self,simbolo):
        nodo1 = Nodo()
        nodo2 = Nodo()
        Transiciontemp = Transicion(nodo1,simbolo,nodo2)
        afntemp = AFN()
        afntemp.add_transicion(Transiciontemp)
        return afntemp
    def ruleor(self,afn1, afn2):
        afntemp = AFN()
        nodo1 = Nodo()
        nodo2 = Nodo()
        Transiciontemp1 = Transicion(nodo1,"ε",afn1.transiciones[0].estadoinicial)
        Transiciontemp2 = Transicion(nodo1,"ε",afn2.transiciones[0].estadoinicial)

        afntemp.add_transicion(Transiciontemp1)
        afntemp.add_transicion(Transiciontemp2)

        for transicion in afn1.transiciones:
            afntemp.add_transicion(transicion)
        for transicion in afn2.transiciones:
            afntemp.add_transicion(transicion)
        

        Transiciontemp3 = Transicion(afn1.transiciones[-1].estadofinal,"ε",nodo2)
        Transiciontemp4 = Transicion(afn2.transiciones[-1].estadofinal,"ε",nodo2)

        afntemp.add_transicion(Transiciontemp3)
        afntemp.add_transicion(Transiciontemp4)

        return afntemp
    
    def reglaKleen(self,afn1):
        afntemp = AFN()
        nodo1 = Nodo()
        nodo2 = Nodo()
        Transiciontemp1 = Transicion(nodo1,"ε",afn1.transiciones[0].estadoinicial)
        afntemp.add_transicion(Transiciontemp1)


        for transicion in afn1.transiciones:
            afntemp.add_transicion(transicion)
                

        Transiciontemp2 = Transicion(afn1.transiciones[-1].estadofinal,"ε",nodo2)
        Transiciontemp3 = Transicion(afn1.transiciones[-1].estadofinal,"ε",afn1.transiciones[0].estadoinicial)
        Transiciontemp4 = Transicion(nodo1,"ε", nodo2)

        afntemp.add_transicion(Transiciontemp2)
        afntemp.add_transicion(Transiciontemp3)
        afntemp.add_transicion(Transiciontemp4)

        return afntemp
    
    def reglaconcat(self,afn1,afn2):
        afntemp = AFN()
        for transicion in afn1.transiciones:
            afntemp.add_transicion(transicion)
        
        estadofinalAFN1 = afn1.transiciones[-1].estadofinal
        estadInicialAFN2 = afn2.transiciones[0].estadoinicial
        
        for transicion in afn2.transiciones:
            if(transicion.estadoinicial == estadInicialAFN2):
                transicion.estadoinicial = estadofinalAFN1
        
        for transicion in afn2.transiciones:
            afntemp.add_transicion(transicion)
        
        return afntemp
    def rulecpositiva(self,afn1):
        afntemp = AFN()
        nodo1 = Nodo()
        nodo2 = Nodo()
        Transiciontemp1 = Transicion(nodo1,"ε",afn1.transiciones[0].estadoinicial)
        afntemp.add_transicion(Transiciontemp1)


        for transicion in afn1.transiciones:
            afntemp.add_transicion(transicion)
                

       
        Transiciontemp3 = Transicion(afn1.transiciones[-1].estadofinal,"ε",afn1.transiciones[0].estadoinicial)
        Transiciontemp2 = Transicion(afn1.transiciones[-1].estadofinal,"ε",nodo2)
        
        afntemp.add_transicion(Transiciontemp3)
        afntemp.add_transicion(Transiciontemp2)
        

        return afntemp
    def reglaOrEpsilon(self,afn1):
        afntemp = self.simbolo("ε")
        return self.ruleor(afn1,afntemp)
    
    def isOperator(self,caracter):
        return caracter == "*" or caracter =="." or caracter == "|" or caracter =="+" or caracter =="?"

    def postfix_to_nfa(self):
        stack = []
        for caracter in self.expresion:
            if not self.isOperator(caracter):
                afn = self.simbolo(caracter)
                stack.append(afn)

            else:
                if caracter =="." or caracter =="|":
                    afn2 = stack.pop()
                    afn1 = stack.pop()
                    if caracter == ".":
                        afn3 = self.reglaconcat(afn1,afn2)
                        stack.append(afn3)

                    elif caracter =="|":
                        afn3 = self.ruleor(afn1,afn2)
                        stack.append(afn3)
                else:
                    if caracter == "*":
                        afntemp = stack.pop()
                        afntemp = self.reglaKleen(afntemp)
                        stack.append(afntemp)

                    elif caracter == "+":
                        afntemp = stack.pop()
                        afntemp = self.rulecpositiva(afntemp)
                        stack.append(afntemp)
                    elif caracter == "?":
                        afntemp = stack.pop()
                        afntemp = self.reglaOrEpsilon(afntemp)
                        stack.append(afntemp)

        

        self.dfa = stack[0]
        return stack[0]

