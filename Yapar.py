from Corazon import *
import graphviz
import copy
from prettytable import *
class Yapar:
    def __init__(self, archivo):
        self.producciones = {}
        self.tokens = []
        self.ingnores = []
        self.producciones_unidas = {}
        self.produccionesfinales = {}
        self.no_terminales = []
        self.terminales = []
        self.estado_inicial = None
        self.identificador_Corazones = []
        self.corazones_instancias = []
        self.corazones = []
        self.corazonesdic = []
        self.corazones_operados = []
        self.datos_temp = []
        self.transiicones_finales = []
        self.enumeracion_gramatica = []
        self.campos = []
        self.tablafinal = None
        
        errors = self.detectar_errores(archivo)
        if len(errors) > 0:
            raise Exception("Error en procesamiento del archivo")
        with open(archivo, 'r') as f:
            produccion_actual = ''
            for linea in f:
                linea = linea.strip()
                if linea.startswith('/*') and linea.endswith('*/'):
                    continue
                if linea.startswith('%token'):
                    self.tokens.extend(linea.split()[1:])
                if linea.startswith('IGNORE'):
                    self.ingnores.extend(linea.split()[1:])

                if linea.endswith(':'):
                    produccion_actual = linea[:-1]
                    self.producciones[produccion_actual] = []
                elif produccion_actual != '':
                    self.producciones[produccion_actual].append(linea)
                if linea.endswith(';'):
                    produccion_actual = ''
            for key, value in self.producciones.items():
                produccion_unida = ' '.join(value[:-1])
                self.producciones_unidas[key] = produccion_unida

            for key,value in self.producciones_unidas.items():
                if '|' in value:
                    self.produccionesfinales[key] = value.split(' | ')
                else:
                    lista = []
                    lista.append(value)
                    self.produccionesfinales[key] = lista
    
    
    def detectar_errores(self, archivo):
        with open(archivo, 'r') as file:
            lineas = file.readlines()

        errores = []

        # Verificar si se encuentra %%
        if "%%\n" not in lineas:
            errores.append("Error: No se encontró la cadena '%%' en el archivo.")

        # Verificar si se encuentra la palabra "token" sin el %
        for linea in lineas:
            if "token" in linea and "%token" not in linea:
                errores.append("Error: La palabra 'token' está presente sin el símbolo '%'. Línea: {}".format(linea.strip()))
        for linea in lineas:
            if "\*" in linea:
                errores.append("Error comentario mal definido")

        if errores:
            print("Se encontraron los siguientes errores:")
            for error in errores:
                print(error)
    
        return errores
    
    def compile(self):
        self.con_terminales()
        self.create_estado_incial()
        firstc = self.expand_grammar()
        self.first(firstc)
        self.draw_afd_Lr0()
        #self.imprimir_transiciones()
        # print("First")
        # firstProudccion = self.compute_first(self.produccionesfinales)
        # print(firstProudccion)
        # print("\n")
        # print("Follow")
        # followPRO = self.compute_follow(self.produccionesfinales)
        # print(followPRO)
        # print("\n")

        self.construccion_tabla()
       

        

    def verificar_tokens(self,lista2):
        self.delete_Ignore()
        cojunto1 = set(self.tokens)
        cojunto2 = set(lista2)

        if cojunto1 == cojunto2:
            print("Los dos archivos comparten los mismos tokens")
            for elemento in cojunto2:
                print("TOKEN "+str(elemento))
            print("\n")
        else:
            elementos_faltantes = cojunto1.symmetric_difference(cojunto2)
            print("Los archivos tienen Tokens Diferentes: ")
            for elemento in elementos_faltantes:
                print("TOKEN "+str(elemento))
            print("\n")

    def delete_Ignore(self):
        self.tokens = [elemento for elemento in self.tokens if elemento not in self.ingnores]

    def con_terminales(self):
        for value in self.producciones_unidas.values():
            palabras = value.split()
            for palabra in palabras:
                if palabra.islower():
                    if palabra not in self.no_terminales:
                        self.no_terminales.append(palabra)
                else:
                    if palabra not in self.terminales and palabra != "|":
                        self.terminales.append(palabra)

        # print(self.no_terminales)
        # print(self.terminales)
    
    def expand_grammar(self):
        prima = self.estado_inicial+"'"
        lista = []
        listaproduccion1 = []
        lista.append(self.estado_inicial)
        prod1 = "."+self.estado_inicial
        listaproduccion1.append(prod1)
        self.estado_inicial = prima
        
        self.produccionesfinales[prima] = lista
        # print("producciones aumentada")
        # print(self.produccionesfinales)
        # print("Nuevo estado inicial")
        # print(self.estado_inicial)
        corazon1 = {}
        corazon1[self.estado_inicial] = listaproduccion1
        # print("Corazon Inciical")
        # print(corazon1)
        corazon = Corazon()
        corazon.cerradura[self.estado_inicial] = listaproduccion1
        corazon.corazon[self.estado_inicial] = listaproduccion1
        return corazon
        
       
        
    def first(self,first):
        primercerradura = self.cerradura(first)
        self.corazones_instancias.append(primercerradura)
        self.corazones.append(primercerradura.corazon)

        for corazon in self.corazones_instancias:
            transiciones = self.get_token_transicion(corazon)
            for transicion in transiciones:
                corazonN = self.Ir_a(corazon,transicion)
                if corazonN.corazon not in self.corazones:
                    self.corazones_instancias.append(corazonN)
                    self.corazones.append(corazonN.corazon)
                    transicion1= []
                    transicion1.append(corazon.id)
                    transicion1.append(transicion)
                    transicion1.append(corazonN.id)
                    corazon.transiciones.append(transicion1)
                else:
                    idCorazon = self.get_corazonid(corazonN.corazon)
                    transicion2 = []
                    transicion2.append(corazon.id)
                    transicion2.append(transicion)
                    transicion2.append(idCorazon)
                    corazon.transiciones.append(transicion2)
        
        diccionario_cambios = {}
        for i in range(len(self.corazones_instancias)):
            
            diccionario_cambios[self.corazones_instancias[i].id] = i
            self.corazones_instancias[i].id = i 
        
        for corazon in self.corazones_instancias:
            for transicion in corazon.transiciones:
                if transicion[0] in diccionario_cambios:
                    transicion[0] = diccionario_cambios[transicion[0]]
                if transicion[2] in  diccionario_cambios:
                    transicion[2] = diccionario_cambios[transicion[2]]
    

            

        
    
    def cerradura(self, I):
        J = copy.deepcopy(I)
        # J.productions = {"term": ['term TIMES factor.']}
        added = True  # flag to indicate whether any new items were added
        while added:
            added = False
            # create a copy of the dictionary to avoid "dictionary changed size during iteration" error
            productions_copy = dict(J.cerradura)
            for key, value in productions_copy.items():
                for prod in value:
                    parts = prod.split()
                    for part in parts:
                        if '.' in part:
                            if part[-1] == '.':
                                next_part_idx = parts.index(part) + 1
                                if next_part_idx == len(parts) or parts[next_part_idx] in self.terminales:
                                    continue
                                else:
                                    part = parts[next_part_idx]
                            sinPunto = part.replace('.', '')
                            # print(sinPunto)
                            if sinPunto in self.produccionesfinales:
                                for new_prod in self.produccionesfinales[sinPunto]:
                                    new_item = '.' + new_prod
                                    if new_item not in J.cerradura.setdefault(sinPunto, []):
                                        J.cerradura.setdefault(sinPunto, []).append(new_item)
                                        added = True
        
        return J

    def move_point(self,string):
        palabras = string.split()
        # print(palabras)
        indice_punto = None
        for i, palabra in enumerate(palabras):
            if '.' in palabra:
                indice_punto = i
                break 
        # print(indice_punto)
        
        if indice_punto == 0 and len(palabras) == 1:
            palabras[0] = palabras[0].replace(".","")
            palabras[0] = palabras[0]+"."
        else:
            palabras[indice_punto] = palabras[indice_punto].replace(".","")
            palabras[indice_punto+1] ="."+ palabras[indice_punto+1]
        return ' '.join(palabras)
    
    def get_corazonid(self,listadiccionario):
        for corazon in self.corazones_instancias:
            if corazon.corazon == listadiccionario:
                return corazon.id
        
    # def get_cerrraduras(self):
    #     for corazon in self.corazones:
    #         print(corazon.cerradura)


    def Ir_a(self, I, X):
        corazontemp =  Corazon()
        copia = copy.deepcopy(I)
        for key, value in copia.cerradura.items():
            for prod in value:
                parts = prod.split()
                
                for i, part in enumerate(parts):
                    if '.' in part:
                        if part.startswith('.'):
                            sinPunto = part.replace('.', '')
                            if sinPunto == X:
                                new_parts = [X + '.' if p == '.' + X else p for p in parts]
                                new_prod = ' '.join(new_parts)
                                corazontemp.cerradura.setdefault(key, []).append(new_prod)
                                corazontemp.corazon.setdefault(key, []).append(new_prod)
                        elif part.endswith('.'):
                            part_idx = parts.index(part)
                            next_part_idx = parts.index(part) + 1
                            if next_part_idx == len(parts):
                                continue
                            next_part = parts[next_part_idx]
                            sinPunto = part.replace('.', '')
                            if next_part == X:
                                next_part += '.'
                                parts[next_part_idx] = next_part
                                parts[part_idx] = sinPunto
                                new_prod = ' '.join(parts)
                                corazontemp.cerradura.setdefault(key, []).append(new_prod)
                                corazontemp.corazon.setdefault(key, []).append(new_prod)

        return self.cerradura(corazontemp)


        

        
    def get_token_transicion(self, I):
        symbols = []
        for value in I.cerradura.values():
            for production in value:
                parts = production.split()
                # print(parts)
                for i, part in enumerate(parts):
                    part = part.strip()
                    if not part:
                        continue
                    if '.' in part:
                        if part.startswith('.'):
                            next_symbol = part[1:]
                            # print(next_symbol)
                            if next_symbol not in symbols:
                                symbols.append(next_symbol)
                        elif part.endswith('.'):
                            if i < len(parts) - 1:
                                next_part = parts[i+1].strip()
                                next_symbol = next_part.split()[0]
                                if next_symbol not in symbols:
                                    symbols.append(next_symbol)
        return symbols

    def add_tranisiciones(self):
        for corazon in self.corazones_instancias:
            for transicon in corazon.transiciones:
                self.transiicones_finales.append(transicon)
        ltemplist = []
        ltemplist.append(1)
        ltemplist.append("$")
        ltemplist.append("aceptacion")

        self.transiicones_finales.append(ltemplist)

    def draw_afd_Lr0(self): #Metodo para dibujar el digrafo con la liberia graphviz
        self.add_tranisiciones()
        g = graphviz.Digraph(graph_attr={'rankdir': 'LR'})  
        nodes = []
        for edge in self.transiicones_finales:
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
        g.render('LR0')
    
    def compute_first(self, producciones):
            first = {nonterminal: [] for nonterminal in producciones}
            
            changes = True
            while changes:
                changes = False
                for nonterminal in producciones:
                    for production in producciones[nonterminal]:
                        symbols = production.split()
                        for i, symbol in enumerate(symbols):
                            if symbol.isupper():
                                # Terminal symbol
                                if symbol not in first[nonterminal]:
                                    first[nonterminal].append(symbol)
                                    changes = True
                                break
                            else:
                                # Nonterminal symbol
                                for first_symbol in first[symbol]:
                                    if first_symbol not in first[nonterminal]:
                                        first[nonterminal].append(first_symbol)
                                        changes = True
                                if 'EPSILON' not in first[symbol]:
                                    break
                        else:
                            # All symbols in the production derive EPSILON
                            if 'EPSILON' not in first[nonterminal]:
                                first[nonterminal].append('EPSILON')
                                changes = True
            return first
    
    
    def compute_follow(self, producciones):
        # Initialize follow sets to empty lists
        follow = {nonterminal: [] for nonterminal in producciones}

        # Initialize the start symbol's follow set to [$]
        start_symbol = list(producciones.keys())[0]
        follow[start_symbol].append('$')

        # Compute the first sets for the grammar
        first = self.compute_first(producciones)

        # Keep track of changes to the follow sets
        changes = True
        while changes:
            changes = False
            for nonterminal in producciones:
                for production in producciones[nonterminal]:
                    symbols = production.split()
                    for i, symbol in enumerate(symbols):
                        if symbol.islower():
                            # Nonterminal symbol
                            if i == len(symbols) - 1:
                                # Last symbol in the production
                                for follow_symbol in follow[nonterminal]:
                                    if follow_symbol not in follow[symbol]:
                                        follow[symbol].append(follow_symbol)
                                        changes = True
                            else:
                                # Not the last symbol in the production
                                if symbols[i+1].islower():
                                    # Next symbol is a nonterminal
                                    for first_symbol in first[symbols[i+1]]:
                                        if first_symbol != 'EPSILON' and first_symbol not in follow[symbol]:
                                            follow[symbol].append(first_symbol)
                                            changes = True
                                    if 'EPSILON' in first[symbols[i+1]]:
                                        for follow_symbol in follow[nonterminal]:
                                            if follow_symbol not in follow[symbol]:
                                                follow[symbol].append(follow_symbol)
                                                changes = True
                                else:
                                    # Next symbol is a terminal
                                    if symbols[i+1] not in first:
                                        # Add the terminal symbol to the first set
                                        first[symbols[i+1]] = [symbols[i+1]]
                                    if symbols[i+1] != 'EPSILON' and symbols[i+1] not in follow[symbol]:
                                        follow[symbol].append(symbols[i+1])
                                        changes = True
                        else:
                            # Terminal symbol
                            continue
        return follow
    
    
    def shift(self,estado,terminal):
        for sublista in self.transiicones_finales:
            if sublista[0] == estado and sublista[1] == terminal:
                return sublista[2]
        return None
        

    def construccion_tabla(self):
        ids = []
        for corazon in self.corazones_instancias:
            ident = corazon.id
            ids.append(ident)
        
        diccionariotabla1 = {}
        fields = self.terminales[:]
        fields.insert(0,"Accion")
        fields.insert(0,"Estado")
        fields.append("$")
        fields.append("ir_A")
        for noterminal in self.no_terminales:
            fields.append(noterminal)
        fieldlen = len(fields)
        
        for i in range(len(ids)):
            diccionariotabla1[i] = [""] * fieldlen
        
        for i in range(len(ids)):
            diccionariotabla1[i][0] = i

        self.terminales.append("$")
        for identificador in ids:
            for terminal in self.terminales:
                numero = self.shift(identificador,terminal)
                if numero is not None:
                    indexList =  fields.index(terminal)
                    # print("Identficador: "+str(identificador))
                    diccionariotabla1[identificador][indexList] = "S"+str(numero)
                    # print(indexList)
                    # print(terminal)
                    # print(numero)
                    # print("\n")
        

        for key, values in self.produccionesfinales.items():
            for value in values:
                lista = []
                lista.append(key)
                lista.append(value)
                self.enumeracion_gramatica.append(lista)
        


        followPRO = self.compute_follow(self.produccionesfinales)
        for corazon in self.corazones_instancias:
            if corazon.id != 1:
                res = self.find_keys_with_period(corazon.cerradura)
                if len(res) != 0:
                    listatok = followPRO[res[0]]
                    produccion = res[1]
                    produccion = produccion.replace(".","")
                    for cadena in listatok:
                        indexList2 = fields.index(cadena)
                        if diccionariotabla1[corazon.id][indexList2] =="":
                            idnum = self.encontrar_posicion_l(res[0],produccion)
                            diccionariotabla1[corazon.id][indexList2] = "R"+str(idnum)
                        elif diccionariotabla1[corazon.id][indexList2].startswith("S"):
                            raise Exception("Existe conflicto Desplazamiento Reduccion")
                        elif diccionariotabla1[corazon.id][indexList2].startswith("R"):
                            raise Exception("Existe conflicto Reduccion Reduccion")
                        
        
        for identificador3 in ids:
            for no_terminal3 in self.no_terminales:
                numero3 = self.shift(identificador3,no_terminal3)
                if numero3 is not None:
                    indexList3 =  fields.index(no_terminal3)
                    diccionariotabla1[identificador3][indexList3] = numero3

        table = PrettyTable()
        table.field_names = fields
        for key, values in diccionariotabla1.items():
            table.add_row(values)
        self.campos = fields
        self.tablafinal = diccionariotabla1
        return diccionariotabla1

    
    

    def crear_y_escribir_archivo(self,outputName,input1,input2):
        codigo = f'''from Yalex import *
from Yapar import *
from prettytable import *
#ejemplo4.yal
#yapa.yalp

#ejemplo5.yal
#yappa2.yalp


yalexInstance = Yalex("{input1}")
res = yalexInstance.getRegexes()
llaves = yalexInstance.getafd()
yapar = Yapar("{input2}")
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
        '''
        with open(outputName, 'w') as file:
            file.write(f"{codigo}")



    def encontrar_posicion_l(self, parametro1, parametro2):
        for i, sublista in enumerate(self.enumeracion_gramatica):
            if sublista[0] == parametro1 and sublista[1] == parametro2:
                return i + 1
        return None

        
    def find_keys_with_period(self,dictionary):
        keys_with_period = []
        for key, values in dictionary.items():
            for value in values:
                if value.endswith('.'):
                    keys_with_period.append(key)
                    keys_with_period.append(value)
                    break
        return keys_with_period
    
        
        

    def imprimir_transiciones(self):
        for corazon in self.corazones_instancias:
            print(corazon.cerradura)
    
    def create_estado_incial(self):
        self.estado_inicial = next(iter(self.produccionesfinales))
        return self.estado_inicial
    def get_tokens(self):
        return self.tokens

    def get_producciones(self):
        return self.produccionesfinales



