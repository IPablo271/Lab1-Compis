from Intp import *
from node import *
from Thompson import *
from subconjuntos import *
from directa import *
from minimizacion import *
from simulacionafd import *
from simulacionafn import *
#Se importan las libreiras necesaria

salir = False

# Expresiones regulares aa(a|b)*(b|a)bbb
while salir == False:
    print("1. Generar afd por medio de thompson")
    print("2. Generar afn por medio de construccion de subcojuntos")
    print("3. Generar afn por construccion directa")
    print("4. Minimizar afn")
    print("5. Simulacion de cadena")
    print("6. Salir")
    opc = input("Ingrese su opcion: ")
    if opc == "1":
        expresion = input("Ingrese la expresion regular: ")
        ift = InfixToPostfix(expresion) #Se crea la instacia del analizador 
        ift.validar_expresion_regular() #Se verifica que la expresion regular cumpla con los parametros
        ift.formatearExpresionRegular() #Se agregan puntos a la expersion
        print(ift.expression)
        result = ift.infix_to_postfix() #Se realiza el postfix de la cadena
        print(result)
        instanceThompson = Thompson(result) #Se crea la instacia de thompson con el resultado del postfix
        afnresult = instanceThompson.postfix_to_nfa() #Se ejecuta el algoritmo de thompson
        afnresult.transicionesToNum()
        afnresult.printAfn() 
        afnresult.draw_graph() #Se dibuja el afn

    elif opc == "2":
        # expresion = input("Ingrese la expresion regular: ")
        expresion = "(a|b)*abb"
        ift = InfixToPostfix(expresion) #Se crea la instacia del analizador 
        ift.validar_expresion_regular() #Se verifica que la expresion regular cumpla con los parametros
        ift.formatearExpresionRegular() #Se agregan puntos a la expersion
        print(ift.expression)
        result = ift.infix_to_postfix() #Se realiza el postfix de la cadena
        print(result)
        instanceThompson = Thompson(result) #Se crea la instacia de thompson con el resultado del postfix
        afnresult = instanceThompson.postfix_to_nfa() #Se ejecuta el algoritmo de thompson
        afnresult.transicionesToNum() #Se crea una lista de las transiciones para poder dibujar el afn
        afnresult.add_nodes()
        afnresult.add_nodes_transiciones()
        instanceSubcojuntos = Subconjuntos(afnresult)
        instanceSubcojuntos.construccion_subconjuntos()
        instanceSubcojuntos.draw_afd()
    
    elif opc == "3":
        expresion = input("Ingrese la expresion regular: ")
        ift = InfixToPostfix(expresion) #Se crea la instacia del analizador 
        ift.validar_expresion_regular() #Se verifica que la expresion regular cumpla con los parametros
        ift.extension_cadena()
        ift.formatearExpresionRegular() #Se agregan puntos a la expersion
        ift.getExpression()
        resultado = ift.infix_to_postfix()
        print(resultado)
        instancedirecta = Directa(resultado)
        instancedirecta.construccion_arbol()
        instancedirecta.construccion_directo()
        instancedirecta.draw_afd()
    elif opc == "4":
        expresion = "(a|b)*abb"
        ift = InfixToPostfix(expresion) #Se crea la instacia del analizador 
        ift.validar_expresion_regular() #Se verifica que la expresion regular cumpla con los parametros
        ift.formatearExpresionRegular() #Se agregan puntos a la expersion
        print(ift.expression)
        result = ift.infix_to_postfix() #Se realiza el postfix de la cadena
        print(result)
        instanceThompson = Thompson(result) #Se crea la instacia de thompson con el resultado del postfix
        afnresult = instanceThompson.postfix_to_nfa() #Se ejecuta el algoritmo de thompson
        afnresult.transicionesToNum() #Se crea una lista de las transiciones para poder dibujar el afn
        afnresult.add_nodes()
        afnresult.add_nodes_transiciones()
        instanceSubcojuntos = Subconjuntos(afnresult)
        instanceSubcojuntos.construccion_subconjuntos()
        instanceminimizacion = Minimizacion(instanceSubcojuntos)
        instanceminimizacion.minimizacion_afd()
        

        
        # ift = InfixToPostfix(expresion) #Se crea la instacia del analizador 
        # ift.validar_expresion_regular() #Se verifica que la expresion regular cumpla con los parametros
        # ift.extension_cadena()
        # ift.formatearExpresionRegular() #Se agregan puntos a la expersion
        # ift.getExpression()
        # resultado = ift.infix_to_postfix()
        # print(resultado)
        # instancedirecta = Directa(resultado)
        # instancedirecta.construccion_arbol()
        # instancedirecta.construccion_directo()
        # instanceminimizacion2 = Minimizacion(instanceSubcojuntos)


        
    elif opc =="5":
        expresion = input("Ingrese la expresion regular: ")
        cadena = input("Ingrese la cadena a simular")

        ift = InfixToPostfix(expresion) #Se crea la instacia del analizador 
        ift.validar_expresion_regular() #Se verifica que la expresion regular cumpla con los parametros
        ift.formatearExpresionRegular() #Se agregan puntos a la expersion
        print(ift.expression)
        result = ift.infix_to_postfix() #Se realiza el postfix de la cadena
        
        instanceThompson = Thompson(result) #Se crea la instacia de thompson con el resultado del postfix
        afnresult = instanceThompson.postfix_to_nfa() #Se ejecuta el algoritmo de thompson
        afnresult.transicionesToNum() #Se crea una lista de las transiciones para poder dibujar el afn
        afnresult.add_nodes()
        afnresult.add_nodes_transiciones()
        instanceSubcojuntos = Subconjuntos(afnresult)
        instanceSubcojuntos.construccion_subconjuntos()
        instancesimulacionafd = SimulacionAfd(instanceSubcojuntos,cadena)
        res = instancesimulacionafd.simulacion_afd()
        print("El resultado de la simulacion por afd es : "+str(res))

        instanceThompson = Thompson(result) #Se crea la instacia de thompson con el resultado del postfix
        afnresult = instanceThompson.postfix_to_nfa() #Se ejecuta el algoritmo de thompson
        afnresult.transicionesToNum()
        afnresult.nodofinal()
        afnresult.add_nodes_transiciones()
        instancesimulacionafn = SimulacionAfn(afnresult,cadena)
        result2 =instancesimulacionafn.simulacion_afn() 
        print("El resultado de la simulacion por afn es: "+str(result2))
        print("")
        
    elif opc == "6":
        salir = True
        print("Saliendo del programa")
    else:
        print("Ingrese un caracter valido")
















