import re
from Intp import *
from directa import *
from simulacionafd import *
from Thompson import *
from subconjuntos import *
from minimizacion import *
from simulacionafn import *
class Yalex:
    def __init__(self, filename):
        self.filename = filename
        self.lines = self._read_file()
        self.tokens = {}
        self.regex_dict = {}
        self.identDict = {}
        self.regex_list = []
        self.regexlist_final = []
        self.diccionario_afd = {}
        self.regexfinal = None
        self.megaregex = None
         
    def _read_file(self):
        with open(self.filename, 'r') as file:
            lines = file.readlines()
        return lines
    
    def check(self):
        listaerrores = []
        with open(self.filename, 'r') as file:
            lines = file.readlines()
        
        for linea in lines:
            #Manejo de errores para la cantidad de {}, (), []
            if linea.count("{") - linea.count("}") != 0:
                listaerrores.append("Eror en la cantidad de simbolos: {} estos deben de estar balanceados ")
            if linea.count("(") - linea.count(")") != 0:
                listaerrores.append("Eror en la cantidad de simbolos: () estos deben de estar balanceados ")
            if linea.count("[") - linea.count("]") != 0:
                listaerrores.append("Eror en la cantidad de simbolos: {} estos deben de estar balanceados ")
            #Manejo de errores en el let 
            if linea.startswith("let"):
                if "=" not in linea.strip():
                    listaerrores.append("Error existene en linea de let, estas no cuentan con un igual")
            if linea.startswith("(*"):
                if linea.endswith("*)") != False:
                    listaerrores.append("Error el comentario no se pudo procesar")
        
        if len(listaerrores) >  1:
            print(listaerrores)
            return listaerrores
        else:
            return listaerrores

    
    
    def getRegexes(self):
        lista = self.check()
        if len(lista) == 0:
            pass
        else:
            raise MultipleErrorsException(lista)
        
        pattern = r"let\s+(\w+)\s*=\s*(.*)"

        for i, line in enumerate(self.lines):
            match = re.match(pattern, line)
            if match:
                self.regex_dict[match.group(1)] = match.group(2)
            if line.startswith("rule"):
                for j,sub_line in enumerate(self.lines[i+1:]):
                    sub_line = sub_line.lstrip()

                    if sub_line.startswith("(*") and re.search(r"\*\)$", sub_line):
                        continue 
                    
                    if "{" in sub_line and "}" in sub_line:
                        brace_content = re.search(r'\{(.+?)\}', sub_line).group(1)
                        self.identDict[brace_content] = ""
                        sub_line = re.sub(r'\{.*?\}', '', sub_line)
                    
                    regex = ""
                    sub_line = re.sub(r'\(\*.*?\*\)', '', sub_line)
                    if j == 0:
                        sub_line = re.sub(r'\{.*?\}', '', sub_line)
                        if sub_line.startswith("|"):
                            sub_line = sub_line[1:].lstrip()
                        regex += sub_line
                        self.regex_list.append(regex.strip())
                        if brace_content:
                            self.identDict[brace_content] = regex.strip()
                            brace_content = None
                    else:
                        if sub_line.startswith("|"):
                            sub_line = re.sub(r'\{.*?\}', '', sub_line)
                            regex += sub_line.strip()[1:]
                            self.regex_list.append(regex.strip())
                            if brace_content:
                                self.identDict[brace_content] = regex.strip()
                                brace_content = None
                        else:
                            break
       
        self.regex_list = [x.replace(' ','') for x in self.regex_list]
        # print("\nEste es la lista con los regex: "+str(self.regex_list))        
    
        for key in reversed(list(self.regex_dict.keys())):
            value = self.regex_dict[key]
            for inner_key, inner_value in self.regex_dict.items():
                if inner_key in value:
                    value = value.replace(inner_key, inner_value)
            self.regex_dict[key] = value
        
        for i in range(len(self.regex_list)):
            for key in self.regex_dict.keys():
                list2 = self.regex_list[i].split(" ")
                for j in range(len(list2)):
                    if key in list2[j]:
                        list2[j] = list2[j].replace(key, self.regex_dict[key]) 
                self.regex_list[i] = " ".join(list2)
        
        
        for i in range(len(self.regex_list)):
            for key in self.regex_dict.keys():
                list2 = self.regex_list[i].split(" ")
                for j in range(len(list2)):
                    if key in list2[j]:
                        list2[j] = list2[j].replace(key, self.regex_dict[key]) 
                self.regex_list[i] = " ".join(list2)
        
        # print("\nDICCIONARIO REGEX - Regexes con sus valores originales:")
        # print(self.regex_dict)

        # print("\nSEGUNDA LISTA - Regexes Con valor Original:")
        # print(self.regex_list)
        # print("Este es el regex list: "+str(self.regex_list))
        
        for i in range(len(self.regex_list)):
            self.regex_list[i] = self.regex_list[i].replace("'","")
            if '.' in self.regex_list[i]:
                self.regex_list[i] = self.regex_list[i].replace(".",",")
            if self.regex_list[i] =="+":
                self.regex_list[i] = "!"
            
        # print("\nTERCERA LISTA - Regexes Con Tokens Reemplazados:")
        # print(self.regex_list)
        
           
        
        for i in range(len(self.regex_list)):
            self.regex_list[i] = re.sub(r'\[ \\t\\n\\r\]', '( |\t|\n|\r)', self.regex_list[i])
            self.regex_list[i] = re.sub(r'\[0-9\]', '(0|1|2|3|4|5|6|7|8|9)', self.regex_list[i])
            self.regex_list[i] = re.sub(r'\[0-4\]', '(0|1|2|3|4)', self.regex_list[i])
            self.regex_list[i] = re.sub(r'\[5-9\]', '(5|6|7|8|9)', self.regex_list[i])
            self.regex_list[i] = re.sub(r'\[a-z\]', '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)', self.regex_list[i])
            self.regex_list[i] = re.sub(r"\[a-zA-Z\]", '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)',self.regex_list[i])
            self.regex_list[i] = re.sub(r"\[a-fA-F\]", '(a|b|c|d|e|f|A|B|C|D|E|F)',self.regex_list[i])
            self.regex_list[i] = re.sub(r'\[xX\]','(x|X)',self.regex_list[i])
            self.regex_list[i] = re.sub(r'\[ \\t\\n\]', '( |\t|\n)', self.regex_list[i])
        
        # print("\nCUARTA LISTA - Regexes Modificados:")
        # print(self.regex_list)
        
            
            
    


        
        
        for i in range(len(self.regex_list)):
            if ') | (' in self.regex_list[i]:
                self.regex_list[i] = self.regex_list[i].replace(") | (",")|(")
        
        # print("\nEsta la lista con los regex remplazados: "+str(self.regex_list)+"\n")

        resultado = ""
        for i in range(len(self.regex_list)):
            resultado += self.regex_list[i]
            if i != len(self.regex_list) - 1:
                resultado += "|"
        resultado = "("+resultado+")"
    
        # print("\nEste es el resultado del megaRegex "+resultado)
        self.megaregex = resultado
       
        copiares = resultado
        ift = InfixToPostfix(copiares) #Se crea la instacia del analizador 
        ift.validar_expresion_regular() #Se verifica que la expresion regular cumpla con los parametros
        ift.formatearExpresionRegular() #Se agregan puntos a la expersion
        result = ift.infix_to_postfix() #Se realiza el postfix de la cadena
        instancedirecta = Directa(result)
        instancedirecta.construccion_arbol()
        instancedirecta.construccion_directo()
        # instancedirecta.draw_afd()

        # instanceThompson = Thompson(result) #Se crea la instacia de thompson con el resultado del postfix
        # afnresult = instanceThompson.postfix_to_nfa() #Se ejecuta el algoritmo de thompson
        # afnresult.transicionesToNum() #Se crea una lista de las transiciones para poder dibujar el afn
        # afnresult.add_nodes()
        # afnresult.add_nodes_transiciones()
        # instanceSubcojuntos = Subconjuntos(afnresult)
        # instanceSubcojuntos.construccion_subconjuntos()
        # instanceSubcojuntos.draw_afd()
        # instanceminimizacion = Minimizacion(instanceSubcojuntos)
        # instanceminimizacion.minimizacion_afd()
        # instanceminimizacion.draw_afd_minimizado()

        return copiares

    def getafd(self):
        llaves = list(self.identDict.keys())

        for i in range(len(llaves)):
            regex = self.regex_list[i]
            valor = llaves[i]  
            ift = InfixToPostfix(regex) #Se crea la instacia del analizador 
            ift.validar_expresion_regular() #Se verifica que la expresion regular cumpla con los parametros
            ift.formatearExpresionRegular() #Se agregan puntos a la expersion
            result = ift.infix_to_postfix() #Se realiza el postfix de la cadena
            instanceThompson = Thompson(result) #Se crea la instacia de thompson con el resultado del postfix
            afnresult = instanceThompson.postfix_to_nfa() #Se ejecuta el algoritmo de thompson
            afnresult.transicionesToNum() #Se crea una lista de las transiciones para poder dibujar el afn
            afnresult.add_nodes()
            afnresult.add_nodes_transiciones()
            instanceSubcojuntos = Subconjuntos(afnresult)
            instanceSubcojuntos.construccion_subconjuntos()
            self.diccionario_afd[valor] = instanceSubcojuntos
    
    def devolverlisatokens(self):
        with open("prueba.txt",'r') as archivo:
            contenido = archivo.read()
            palabras = contenido.split()
        
        diccionario_respuesta = {}
        palabras_econtradas = []
        for palabra in palabras:
            for clave,valor in self.diccionario_afd.items():
                simul = SimulacionAfd(valor,palabra)
                res = simul.simulacion_afd()
                if res == True:
                    diccionario_respuesta[palabra] = clave
                    palabras_econtradas.append(palabra)
                    break
    


       

    
    def simulacion_afd(self,regex):
        while True:
            print("1. Simular cadena")
            print("2. Salir de la simulacion")
            opc = input("Ingrese la opcion que desea: ")
            if opc == "1":

                cadena = input("Ingrese la cadena a simular: ")

                ift = InfixToPostfix(regex) #Se crea la instacia del analizador 
                ift.validar_expresion_regular() #Se verifica que la expresion regular cumpla con los parametros
                ift.formatearExpresionRegular() #Se agregan puntos a la expersion
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

            else:
                break
    def crear_y_escribir_archivo(self,outputName):
        codigo = f'''from simulacionafd import *
from prettytable import PrettyTable
from Yalex import Yalex
import re
yalexInstance = Yalex('{self.filename}')
res = yalexInstance.getRegexes()
yalexInstance.getafd()
megaautomata = yalexInstance.megaregex
dic_afd = yalexInstance.diccionario_afd
def main():
    listakeys = []
    listavalues = []
    txt = input("Ingrese el nombre del archivo: ")
    with open(txt,'r') as archivo:
            contenido = archivo.read()
    palabras = re.findall(r'"(?:\.|[^"\]])*"|\S+',contenido)
    for palabra in palabras:
        if palabra == "+":
            palabra = "!"
        else:
            pass
    palabras_econtradas = []
    for palabra in palabras:
        for clave,valor in dic_afd.items():
            simul = SimulacionAfd(valor,palabra)
            res = simul.simulacion_afd()
            if res == True:
                listakeys.append(palabra)
                listavalues.append(clave)
                palabras_econtradas.append(palabra)
                break
    if palabras == palabras_econtradas:
        print("Lista de Tokens")
        tabla = PrettyTable()
        tabla.field_names = ["Token", "Valor"]
        for i in range(len(listakeys)):
            key = listakeys[i]
            value = listavalues[i]
            tabla.add_row([key, value])
        print(tabla)

    else:
        print('Se encontro un error de reconocimento de tokens')
        lista1_set = set(palabras)
        lista2_set = set(palabras_econtradas)

        dif = lista1_set - lista2_set

        resultado = list(dif)
        
        for i in range(len(resultado)):
            print("El token "+resultado[i]+" No se pudo reconocer")
if __name__ == "__main__":
    main()
        '''
        with open(outputName, 'w') as file:
            file.write(f"{codigo}")
        
        

class MultipleErrorsException(Exception):
    pass