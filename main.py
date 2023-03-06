from Intp import *
from node import *
from Thompson import *
from subconjuntos import *
#Se importan las libreiras necesaria


ift = InfixToPostfix("aa(a|b)*(b|a)bbb") #Se crea la instacia del analizador 
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
afnresult.add_nodes_transiciones()


instanceSubcojuntos = Subconjuntos(afnresult)

instanceSubcojuntos.construccion_subconjuntos()
instanceSubcojuntos.draw_afd()



afnresult.draw_graph() #Se dibuja el afn














