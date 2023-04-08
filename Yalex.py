import re
from Intp import *
from directa import *
from simulacionafd import *
from Thompson import *
from subconjuntos import *

class Yalex:
    def __init__(self, filename):
        self.filename = filename
        self.lines = self._read_file()
        self.tokens = {}
        self.regex_dict = {}
        self.identDict = {}
        self.regex_list = []
        self.regexlist_final = []
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
                    listaerrores.append("Error existen lienas las cuales no tienen un igual")
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
                      # Remove comments enclosed in '(**)'
                    # sub_line = re.sub(r'\(\*.*?\*\)', '', sub_line)
                    sub_line = sub_line.lstrip()

                    if sub_line.startswith("(*") and re.search(r"\*\)$", sub_line):
                        continue  # skip to next iteration if line is a comment
                    
                    # check if the line has curly braces '{}'
                    if "{" in sub_line and "}" in sub_line:
                        # extract the content inside the curly braces
                        brace_content = re.search(r'\{(.+?)\}', sub_line).group(1)
                        # use the content inside the braces as the key in the dictionary
                        self.identDict[brace_content] = ""
                        # remove the content inside the braces from the line
                        sub_line = re.sub(r'\{.*?\}', '', sub_line)
                    
                    regex = ""
                     # Remove comments enclosed in '(**)'
                    sub_line = re.sub(r'\(\*.*?\*\)', '', sub_line)
                    if j == 0:
                        # Remove actions enclosed in '{}'
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
                            # Remove actions enclosed in '{}'
                            sub_line = re.sub(r'\{.*?\}', '', sub_line)
                            regex += sub_line.strip()[1:]
                            self.regex_list.append(regex.strip())
                            # print(f"Found regex: {regex}")
                            if brace_content:
                                self.identDict[brace_content] = regex.strip()
                                brace_content = None
                        else:
                            break

        # print("\nDICCIONARIO IDENT - Identificacion de los tokens:")
        # print(self.identDict)
        self.diccionario_val = self.identDict.copy()

        
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
        

        # print("Este es el regex list: "+str(self.regex_list))
        
        for i in range(len(self.regex_list)):
            self.regex_list[i] = self.regex_list[i].replace("'","")
            if '.' in self.regex_list[i]:
                self.regex_list[i] = self.regex_list[i].replace(".",",")

        
           
        # print("\nEste es el regex list con las comas remplazadas: "+str(self.regex_list))

        for i in range(len(self.regex_list)):
            self.regex_list[i] = re.sub(r'\[ \\t\\n\\r\]', '( |\t|\n|\r)', self.regex_list[i])
            self.regex_list[i] = re.sub(r'\[0-9\]', '(0|1|2|3|4|5|6|7|8|9)', self.regex_list[i])
            self.regex_list[i] = re.sub(r'\[a-z\]', '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)', self.regex_list[i])
            self.regex_list[i] = re.sub(r"\[a-zA-Z\]", '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)',self.regex_list[i])
            self.regex_list[i] = re.sub(r'\[ \\t\\n\]', '( |\t|\n)', self.regex_list[i])
        
        for i in range(len(self.regex_list)):
            if '((' in self.regex_list[i]:
                self.regex_list[i] = self.regex_list[i].replace('((','(')
                self.regex_list[i] = self.regex_list[i].replace(')|', '|')


        # print("Esta es la lista final de regex: "+str(self.regex_list)+"\n")
        
        resultado = ""
        for i in range(len(self.regex_list)):
            resultado += self.regex_list[i]
            if i != len(self.regex_list) - 1:
                resultado += "|"
        
    
        print("\nEste es el resultado del megaRegex "+resultado)
        self.megaregex = resultado
       
        copiares = resultado
        ift = InfixToPostfix(resultado) #Se crea la instacia del analizador 
        ift.validar_expresion_regular() #Se verifica que la expresion regular cumpla con los parametros
        ift.extension_cadena()
        ift.formatearExpresionRegular() #Se agregan puntos a la expersion
        ift.getExpression()
        resultado = ift.infix_to_postfix()
        instancedirecta = Directa(resultado)
        instancedirecta.construccion_arbol()
        instancedirecta.construccion_directo()
        instancedirecta.draw_afd()

        return copiares
    
    def simulacion_afd(self,regex):
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


class MultipleErrorsException(Exception):
    pass