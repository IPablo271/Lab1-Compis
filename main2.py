from Intp import *
from node import *
from Thompson import *
#Se importan las libreiras necesaria


ift = InfixToPostfix("(a|b)*abb") #Se crea la instacia del analizador 
ift.validar_expresion_regular() #Se verifica que la expresion regular cumpla con los parametros
print(ift.expression)
ift.formatearExpresionRegular() #Se agregan puntos a la expersion
print(ift.expression)
result = ift.infix_to_postfix() #Se realiza el postfix de la cadena
print(result)













