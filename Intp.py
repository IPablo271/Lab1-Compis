
'''
Universidad del valle de Guatemala
Nombre: Pablo Gonzalez
Carnet: 20362
Proposito de clase: Esta clase tiene como proposito
poder convertir una expresion infix to postfix y verificar
si esta tiene error para poder procesar la informacion.
'''
class InfixToPostfix:
    def __init__(self,expression): #Constructor del programa
        self.expression = expression
    
    def valid_construction_regex(self): #Metodo para verificar que la expresion no tenga una de estas diferentes combinaciones imbalidas.
        invalid_combinations = ['**', '+*', '*+', '(|', '|)', '||', '(.', '.)', '..', '.+', '+.', '(*', '(+', '??']
        #Check for invalid combinations
        for i in invalid_combinations:
            if i in self.expression:
                index = self.expression.find(i)
                raise Exception('La cadena cuenta con una combinacion de operadores invalida ')
    
    def null_regex(self): #Se verifica que la cadena no este vacia
        if not self.expression:
            raise Exception('La cadena esta vacia')
        else:
            return False
    def verificar_parentesis(self): #Metodo para verificar que la cadena tenga la misma cantidad de parentesis cerrados que parentesis abiertos
        contador = 0

        for caracter in self.expression:
            if caracter == '(':
                contador += 1
            elif caracter == ')':
                contador -= 1
                if contador < 0:
                    return False

        if contador == 0:
            return False
        else:
            raise Exception("La cadena tien una cantidad desbalanceada de parentesis")
    def verificar_cadena(self): #Metodo para verificar que la cadena no empiece con un operador
        operadores = [".","?","|","*","+",")"]
        if self.expression[0] in operadores:
            raise Exception("La cadena cuenta con un operador al inicio de la cadena")
        else:
            return False
    

    def validar_expresion_regular(self): #Metodo que unifica todos los posbles errore y retina 1 si no hay error
        self.valid_construction_regex()
        self.null_regex()
        self.verificar_parentesis()
        self.verificar_cadena()
        return 1
    def extension_cadena(self):
        self.expression = self.expression + "#"
        return self.expression
    

    def formatearExpresionRegular(self): #metodo para poder agregar puntos a la expresion
        respuesta = ''
        opera = set(["|", "*", "+", "?"])
        operadb = set(["|"])
        for i in range(len(self.expression)):
            caracter = self.expression[i]
            if i + 1 < len(self.expression):
                siguienteCaracter = self.expression[i + 1]
                respuesta += caracter
                if caracter != '(':
                    if siguienteCaracter != ')':
                        if siguienteCaracter not in opera:
                            if caracter not in operadb:
                                respuesta += '.'

        self.expression = respuesta + self.expression[-1]
        return 1
    def getExpression(self):
        # modificamos el regex para que no tenga ?
        if '?' in self.expression:
            self.expression = self.expression.replace('?', '|ε')
            self.expression = self.expression.replace('.|ε', '|ε.')
            parts = self.expression.split('.')
            for i in range(len(parts)):
                if '|ε' in parts[i]:
                    parts[i] = f"({parts[i]})"
            self.expression = ".".join(parts)

        # modificamos el regex para que no tenga +
        if '+' in self.expression:
            parts = self.expression.split('.')
            new_parts = []
            for i, part in enumerate(parts):
                if '+' in part:
                    if '(' in part and ')' in part and part.index('(') < part.index('+') < part.index(')'):
                        subparts = part[part.index(
                            '(') + 1:part.index(')')].split('+')
                        new_part = f"({subparts[0]}.{subparts[0]}*)"
                        new_parts.append(new_part)
                    else:
                        subparts = part.split('+')
                        new_part = f"{subparts[0]}.{subparts[0]}*"
                        new_parts.append(new_part)
                else:
                    new_parts.append(part)
            self.expression = ".".join(new_parts)

        return self.expression
   

    def infix_to_postfix(self): #Metodo que convierte el infix a postfix 
        precedence = {"|": 1, ".": 2, "*": 3}
        stack = []
        postfix = []
        for c in self.expression:
            if c == "(":
                stack.append(c)
            elif c == ")":
                while stack and stack[-1] != "(":
                    postfix.append(stack.pop())
                stack.pop() 
            elif c in precedence:
                while stack and stack[-1] != "(" and precedence[c] <= precedence[stack[-1]]:
                    postfix.append(stack.pop())
                stack.append(c)
            else:
                postfix.append(c)

        while stack:
            postfix.append(stack.pop())

        return "".join(postfix)


