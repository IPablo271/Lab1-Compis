from Intp import *
from node import *
from Thompson import *
from subconjuntos import *
#Se importan las libreiras necesaria


ift = InfixToPostfix("(a|b)*abb") #Se crea la instacia del analizador 
ift.validar_expresion_regular() #Se verifica que la expresion regular cumpla con los parametros
ift.formatearExpresionRegular() #Se agregan puntos a la expersion
print(ift.expression)
result = ift.infix_to_postfix() #Se realiza el postfix de la cadena
print(result)
instanceThompson = Thompson(result) #Se crea la instacia de thompson con el resultado del postfix
afnresult = instanceThompson.postfix_to_nfa() #Se ejecuta el algoritmo de thompson
afnresult.transicionesToNum() #Se crea una lista de las transiciones para poder dibujar el afn
#afnresult.printAfn() #Se imprime el afn con con sus transiciones

afnresult.add_nodes()


instanceSubcojuntos = Subconjuntos(afnresult)

listai = []
listai.append(instanceSubcojuntos.nodos_afd[0])

subconjunto1 = instanceSubcojuntos.eclousere(listai)



mover_a = instanceSubcojuntos.mover(subconjunto1,"a")
mover_b = instanceSubcojuntos.mover(subconjunto1,"b")

subconjunto2 = instanceSubcojuntos.eclousere(mover_a)
subconjunto3 = instanceSubcojuntos.eclousere(mover_b)

afnresult.draw_graph() #Se dibuja el afn














