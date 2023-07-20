from Yalex import *
from Yapar import *
from prettytable import *
#ejemplo4.yal
#yapa.yalp

#ejemplo5.yal
#yappa2.yalp


yalexInstance = Yalex("ejemplo3.yal")
res = yalexInstance.getRegexes()
llaves = yalexInstance.getafd()
yapar = Yapar("yapa.yalp")
yapar.verificar_tokens(llaves)
yapar.compile()

gototable = yapar.tablafinal
campos = yapar.campos
enumeracion_gramatica = yapar.enumeracion_gramatica

archivo = input("Ingrese el archivo de tokens yapar a analizar: ")





def main(gototable,archivo,campos,enumeracion_gramatica):
        
       
        with open(archivo,'r') as archivo:
            contenido = archivo.read()
            data = contenido.split()
        
        data.append("$")
        stack = []
        stack.append(0)
        fields2 = ["Iteracion","Pila","Entrada","Accion"]
        ietraciones = []
        lista_errores = []
        
        contador = 0
        #print(self.campos)
        # print(gototable)
        condicion = True
        while condicion:
            
            ultimodato = stack[-1]
            dato = data[0]
            if dato not in campos:
                raise Exception("El toquen "+str(dato) +" que se esta buscando no se encuentra en la tabla")

            idx = campos.index(dato)

            lista = []
           
            if gototable[ultimodato][idx] == "Saceptacion":
                lista.append(contador)
                if len(stack) == 1:
                    datoStack = str(stack[0])
                    lista.append(datoStack)
                else:
                    datosstack =[str(numero) for numero in stack]
                    Pilas = " ".join(datosstack)
                    lista.append(Pilas)
                Entradas = " ".join(data)
                lista.append(Entradas)
                accion = "Aceptar"
                lista.append(accion)
                ietraciones.append(lista)

                condicion = False
                break

            elif gototable[ultimodato][idx].startswith("S"):
                lista.append(contador)
                if len(stack) == 1:
                    datoStack = str(stack[0])
                    lista.append(datoStack)
                else:
                    datosstack =[str(numero) for numero in stack]
                    Pilas = " ".join(datosstack)
                    lista.append(Pilas)
                Entradas = " ".join(data)
                lista.append(Entradas)
                string =  gototable[ultimodato][idx]
                numero = string[1:] if string[0].upper() == "S" and string[1:].isdigit() else None
                
                
                
                
                contador += 1
                accion = "Desplazar mediante: "+str(numero)
                lista.append(accion)
                ietraciones.append(lista)
                stack.append(int(numero))

                if len(stack) == 0:
                    raise Exception("No se puede operar el pop debido a que el tamano del stack es 0")
                data.pop(0)
                
            elif gototable[ultimodato][idx].startswith("R"):
                lista.append(contador)
                if len(stack) == 1:
                    datoStack = str(stack[0])
                    lista.append(datoStack)
                else:
                    datosstack =[str(numero) for numero in stack]
                    Pilas = " ".join(datosstack)
                    lista.append(Pilas)
                Entradas = " ".join(data)
                lista.append(Entradas)
                

                
                string =  gototable[ultimodato][idx]
                numero = string[1:] if string[0].upper() == "R" and string[1:].isdigit() else None
                numero = int(numero)
                

                produccionR = enumeracion_gramatica[numero-1][1]
                encabezadoProduccionR = enumeracion_gramatica[numero-1][0]
                listaR = produccionR.split()
                if len(stack) < len(listaR):
                    raise Exception("No se puede operar el pop debido a que el tamano del stack es menor al tmano de los simmbolos en la produccion")
                for i in range(len(listaR)):
                    stack.pop()
                
                ultimodato2 = stack[-1]
                # print(encabezadoProduccionR)
                # print("Este es el ultimodato despues de hacer el for de pop "+str(ultimodato2))

                idx2 = campos.index(encabezadoProduccionR)
                numappend = gototable[ultimodato2][idx2]
                # print(numappend)
                contador += 1
                accion = "Reducir mediante: "+str(encabezadoProduccionR)+ " -> " +str(produccionR)
                lista.append(accion)
                ietraciones.append(lista)
                stack.append(numappend)
            else:
                print(ultimodato)
                print(idx)
                print("Este es el dato: "+str(gototable[ultimodato][idx]))

                tableIteraciones = PrettyTable()
                tableIteraciones.field_names = fields2
                for iteracion in ietraciones:
                    tableIteraciones.add_row(iteracion)
                print(" ")
                print("Error en el analisis ")
                print(tableIteraciones)
                condicion = False
                raise Exception("No se pudo encontrar la sustitucion o el Reduce en la tabla")
        table = PrettyTable()
        table.field_names = campos
        for key, values in gototable.items():
            table.add_row(values)
        print(table)
        print(" ")
        print("Analisis realizado con exito ")
        tableIteraciones = PrettyTable()
        tableIteraciones.field_names = fields2
        for iteracion in ietraciones:
            tableIteraciones.add_row(iteracion)
        print(" ")
        print(tableIteraciones)

if __name__ == "__main__":
    
    main(gototable,archivo,campos,enumeracion_gramatica)
        